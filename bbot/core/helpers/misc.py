import os
import atexit
import psutil
import random
import shutil
import signal
import string
import logging
import ipaddress
import wordninja
from pathlib import Path
from contextlib import suppress
import tldextract as _tldextract
from urllib.parse import urlparse, quote  # noqa F401
from hashlib import sha1 as hashlib_sha1
from itertools import combinations, islice

from .url import *  # noqa F401
from .regexes import word_regexes, event_type_regexes

log = logging.getLogger("bbot.core.helpers.misc")


def is_dns_name(d):
    """
    "evilcorp.com" --> True
    "bob@evilcorp.com" --> False
    """
    for r in event_type_regexes["DNS_NAME"]:
        if r.match(d):
            return True
    return False


def is_domain(d):
    """
    "evilcorp.co.uk" --> True
    "www.evilcorp.co.uk" --> False
    """
    extracted = tldextract(d)
    if extracted.domain and not extracted.subdomain:
        return True
    return False


def is_subdomain(d):
    """
    "www.evilcorp.co.uk" --> True
    "evilcorp.co.uk" --> False
    """
    extracted = tldextract(d)
    if extracted.domain and extracted.subdomain:
        return True
    return False


def split_host_port(d):
    """
    "evilcorp.com:443" --> ("evilcorp.com", 443)
    "192.168.1.1:443" --> (IPv4Address('192.168.1.1'), 443)
    "[dead::beef]:443" --> (IPv6Address('dead::beef'), 443)
    """
    if not "://" in d:
        d = f"d://{d}"
    parsed = urlparse(d)
    port = None
    host = None
    with suppress(ValueError):
        if parsed.port is None:
            if parsed.scheme == "https":
                port = 443
            elif parsed.scheme == "http":
                port = 80
        else:
            port = int(parsed.port)
    with suppress(ValueError):
        host = parsed.hostname
    return make_ip_type(host), port


def parent_domain(d):
    """
    "www.internal.evilcorp.co.uk" --> "internal.evilcorp.co.uk"
    "www.evilcorp.co.uk" --> "evilcorp.co.uk"
    "evilcorp.co.uk" --> "evilcorp.co.uk"
    """
    if is_subdomain(d):
        return ".".join(str(d).split(".")[1:])
    return d


def domain_parents(d, include_self=False):
    """
    "test.www.evilcorp.co.uk" --> ["www.evilcorp.co.uk", "evilcorp.co.uk"]
    """
    parent = str(d)
    if include_self:
        yield parent
    while 1:
        parent = parent_domain(parent)
        if is_subdomain(parent):
            yield parent
            continue
        elif is_domain(parent):
            yield parent
        break


def ip_network_parents(i, include_self=False):
    """
    "192.168.1.1" --> [192.168.1.0/31, 192.168.1.0/30 ... 128.0.0.0/1, 0.0.0.0/0]
    """
    net = ipaddress.ip_network(i, strict=False)
    for i in range(net.prefixlen - (0 if include_self else 1), -1, -1):
        yield ipaddress.ip_network(f"{net.network_address}/{i}", strict=False)


def is_ip(d, version=None):
    """
    "192.168.1.1" --> True
    "evilcorp.com" --> False
    """
    if type(d) in (ipaddress.IPv4Address, ipaddress.IPv6Address):
        if version is None or version == d.version:
            return True
    try:
        ip = ipaddress.ip_address(d)
        if version is None or ip.version == version:
            return True
    except Exception:
        pass
    return False


def is_ip_type(i):
    """
    IPv6Address('dead::beef') --> True
    IPv4Network('192.168.1.0/24') --> True
    "192.168.1.0/24" --> False
    """
    return hasattr(i, "is_multicast")


def is_email(d):
    """
    "bob@evilcorp.com" --> True
    "evilcorp.com" --> False
    """
    for r in event_type_regexes["EMAIL_ADDRESS"]:
        if r.match(str(d)):
            return True
    return False


def make_ip_type(s):
    """
    "dead::beef" --> IPv6Address('dead::beef')
    "192.168.1.0/24" --> IPv4Network('192.168.1.0/24')
    "evilcorp.com" --> "evilcorp.com"
    """
    # IP address
    with suppress(Exception):
        return ipaddress.ip_address(str(s).strip())
    # IP network
    with suppress(Exception):
        return ipaddress.ip_network(str(s).strip(), strict=False)
    return s


def host_in_host(host1, host2):
    """
    Is host1 included in host2?
        "www.evilcorp.com" in "evilcorp.com"? --> True
        "evilcorp.com" in "www.evilcorp.com"? --> False
        IPv6Address('dead::beef') in IPv6Network('dead::/64')? --> True
        IPv4Address('192.168.1.1') in IPv4Network('10.0.0.0/8')? --> False
    """

    if not host1 or not host2:
        return False

    # check if hosts are IP types
    host1_ip_type = is_ip_type(host1)
    host2_ip_type = is_ip_type(host2)
    # if both hosts are IP types
    if host1_ip_type and host2_ip_type:
        if not host1.version == host2.version:
            return False
        host1_net = ipaddress.ip_network(host1)
        host2_net = ipaddress.ip_network(host2)
        return host1_net.subnet_of(host2_net)

    # else hostnames
    elif not (host1_ip_type or host2_ip_type):
        host2_len = len(host2.split("."))
        host1_truncated = ".".join(host1.split(".")[-host2_len:])
        return host1_truncated == host2

    return False


def sha1(data):
    """
    sha1("asdf").hexdigest() --> "3da541559918a808c2402bba5012f6c60b27661c"
    """
    return hashlib_sha1(smart_encode(data))


def smart_decode(data):
    """
    Turn data into a string without complaining about it
        b"asdf" --> "asdf"
        "asdf" --> "asdf"
    """
    if type(data) == bytes:
        return data.decode("utf-8", errors="ignore")
    else:
        return str(data)


def smart_encode(data):
    """
    Turn data into bytes without complaining about it
        "asdf" --> b"asdf"
    """
    if type(data) == bytes:
        return data
    return str(data).encode("utf-8", errors="ignore")


def tldextract(data):
    """
    "www.evilcorp.co.uk" --> ExtractResult(subdomain='www', domain='evilcorp', suffix='co.uk')
    """
    return _tldextract.extract(smart_decode(data))


def split_domain(hostname):
    """
    "www.internal.evilcorp.co.uk" --> ("www.internal", "evilcorp.co.uk")
    """
    parsed = tldextract(hostname)
    return (parsed.subdomain, parsed.registered_domain)


rand_pool = string.ascii_lowercase + string.digits


def rand_string(length=10):
    """
    rand_string() --> "c4hp4i9jzx"
    rand_string(20) --> "ap4rsdtg5iw7ey7y3oa5"
    rand_string(30) --> "xdmyxtglqf0z3q8t46n430kesq68yu"
    """
    return "".join([random.choice(rand_pool) for _ in range(int(length))])


def extract_words(data, max_length=100):
    """
    Intelligently extract words from given data
    Returns set() of extracted words
    """
    words = set()
    data = smart_decode(data)

    for r in word_regexes:
        for word in set(r.findall(data)):
            # blacklanternsecurity
            if len(word) <= max_length:
                words.add(word)

    # blacklanternsecurity --> ['black', 'lantern', 'security']
    max_slice_length = 3
    for word in list(words):
        subwords = wordninja.split(word)
        # blacklanternsecurity --> ['black', 'lantern', 'security', 'blacklantern', 'lanternsecurity']
        for s, e in combinations(range(len(subwords) + 1), 2):
            if e - s <= max_slice_length:
                subword_slice = "".join(subwords[s:e])
                words.add(subword_slice)
        # blacklanternsecurity --> bls
        if len(subwords) > 1:
            words.add("".join([c[0] for c in subwords if len(c) > 0]))

    return words


def kill_children(parent_pid=None, sig=signal.SIGTERM):
    """
    Forgive me father for I have sinned
    """
    try:
        parent = psutil.Process(parent_pid)
    except psutil.NoSuchProcess:
        log.warning(f"No such PID: {parent_pid}")
    log.debug(f"Killing children of process ID {parent.pid}")
    children = parent.children(recursive=True)
    for child in children:
        log.debug(f"Killing child with PID {child.pid}")
        if child.name != "python":
            child.send_signal(sig)


def str_or_file(s):
    """
    "file.txt" --> ["file_line1", "file_line2", "file_line3"]
    "not_a_file" --> ["not_a_file"]
    """
    try:
        with open(s, errors="ignore") as f:
            for line in f:
                yield line.rstrip("\r\n")
    except OSError:
        yield s


def chain_lists(l, try_files=False, msg=None):
    """
    Chain together list, splitting entries on comma
        - Optionally try to open entries as files and add their content to the list
        - Used for parsing a list of arguments that may include space and/or comma-separated values
        - ["a", "b,c,d"] --> ["a", "b", "c", "d"]
        - try_files=True:
            - ["a,file.txt", "c,d"] --> ["a", "f_line1", "f_line2", "f_line3", "c", "d"]
    """
    final_list = dict()
    for entry in l:
        for s in entry.split(","):
            f = s.strip()
            f_path = Path(f).resolve()
            if try_files and f_path.is_file():
                if msg is not None:
                    msg = str(msg).format(filename=f_path)
                    log.info(msg)
                for line in str_or_file(f):
                    final_list[line] = None
            else:
                final_list[f] = None

    return list(final_list)


def list_files(directory, filter=lambda x: True):
    """
    "/tmp/test" --> ["file1.txt", "file2.txt"]
    """
    directory = Path(directory)
    if directory.is_dir():
        for file in os.listdir(directory):
            file = directory / file
            if file.is_file() and filter(file):
                yield file


def rm_at_exit(path):
    """
    Removes a file automatically when BBOT exits
    """
    atexit.register(_rm_at_exit, path)


def _rm_at_exit(path):
    with suppress(Exception):
        Path(path).unlink(missing_ok=True)


def read_file(filename):
    """
    "/tmp/file.txt" --> ["file_line1", "file_line2", "file_line3"]
    """
    with open(filename, errors="ignore") as f:
        for line in f:
            yield line.rstrip("\r\n")


def gen_numbers(n, padding=2):
    """
    n=5 --> ['0', '00', '01', '02', '03', '04', '1', '2', '3', '4']
    n=3, padding=3 --> ['0', '00', '000', '001', '002', '01', '02', '1', '2']
    n=5, padding=1 --> ['0', '1', '2', '3', '4']
    """
    results = set()
    for i in range(n):
        for p in range(1, padding + 1):
            results.add(str(i).zfill(p))
    return results


def make_netloc(host, port):
    """
    ("192.168.1.1", 443) --> "192.168.1.1:443"
    ("evilcorp.com", 80) --> "evilcorp.com:80"
    ("dead::beef", 443) --> "[dead::beef]:443"
    """
    if is_ip(host, version=6):
        host = f"[{host}]"
    return f"{host}:{port}"


def which(*executables):
    """
    "python" --> "/usr/bin/python"
    """
    for e in executables:
        location = shutil.which(e)
        if location:
            return location


def validate_port(port):
    """
    443 --> True
    8080 --> True
    77777 --> False
    -4 --> False
    """
    try:
        return 0 <= int(str(port)) <= 65535
    except Exception:
        return False


sentinel = object()


def search_dict_by_key(key, d):
    """
    Recursively search a dictionary "d" for a key matching "k" and return the corresponding value
    raises KeyError if key does not exist
    """
    v = _search_dict_by_key(key, d)
    if v is not sentinel:
        return v
    raise KeyError(key)


def _search_dict_by_key(key, d):
    if isinstance(d, dict):
        if key in d:
            return d[key]
        for k, v in d.items():
            item = _search_dict_by_key(key, v)
            if item is not sentinel:
                return item
    elif isinstance(d, list):
        for v in d:
            item = _search_dict_by_key(key, v)
            if item is not sentinel:
                return item
    return sentinel


def grouper(iterable, n):
    """
    >>> list(grouper('ABCDEFG', 3))
    [['A', 'B', 'C'], ['D', 'E', 'F'], ['G']]
    """
    iterable = iter(iterable)
    return iter(lambda: list(islice(iterable, n)), [])


def split_list(alist, wanted_parts=2):
    """
    >>> split_list([1,2,3,4,5])
    [[1, 2], [3, 4, 5]]
    """
    length = len(alist)
    return [alist[i * length // wanted_parts : (i + 1) * length // wanted_parts] for i in range(wanted_parts)]
