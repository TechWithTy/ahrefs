from ._requests import CrawlerIpAddressesRequest, CrawlerIpRangesRequest
from ..client import AhrefsClient


def handle_crawler_ip_addresses(payload: CrawlerIpAddressesRequest, client: AhrefsClient):
    extra = payload.extra or {}
    return client.get_crawler_ip_addresses(**extra)


def handle_crawler_ip_ranges(payload: CrawlerIpRangesRequest, client: AhrefsClient):
    extra = payload.extra or {}
    return client.get_crawler_ip_ranges(**extra)
