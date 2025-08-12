from ._requests import (
    ProjectsRequest,
    CreateProjectRequest,
    KeywordsGetRequest,
    KeywordsPutRequest,
    KeywordsDeleteRequest,
    CompetitorsGetRequest,
    CompetitorsAddRequest,
    CompetitorsDeleteRequest,
    LocationsAndLanguagesRequest,
    KeywordListsRequest,
)
from ..client import AhrefsClient


# Projects

def handle_projects(_: ProjectsRequest, client: AhrefsClient):
    return client.get_projects()


def handle_create_project(payload: CreateProjectRequest, client: AhrefsClient):
    extra = payload.extra or {}
    return client.create_project(name=payload.name, target=payload.target, **extra)


# Keywords

def handle_keywords_get(payload: KeywordsGetRequest, client: AhrefsClient):
    extra = payload.extra or {}
    return client.get_keywords(project_id=payload.project_id, **extra)


def handle_keywords_put(payload: KeywordsPutRequest, client: AhrefsClient):
    extra = payload.extra or {}
    return client.put_keywords(project_id=payload.project_id, keywords=payload.keywords, **extra)


def handle_keywords_delete(payload: KeywordsDeleteRequest, client: AhrefsClient):
    extra = payload.extra or {}
    return client.delete_keywords(project_id=payload.project_id, keywords=payload.keywords, **extra)


# Competitors

def handle_competitors_get(payload: CompetitorsGetRequest, client: AhrefsClient):
    extra = payload.extra or {}
    return client.get_competitors(project_id=payload.project_id, **extra)


def handle_competitors_add(payload: CompetitorsAddRequest, client: AhrefsClient):
    extra = payload.extra or {}
    return client.add_competitors(project_id=payload.project_id, competitors=payload.competitors, **extra)


def handle_competitors_delete(payload: CompetitorsDeleteRequest, client: AhrefsClient):
    extra = payload.extra or {}
    return client.delete_competitors(project_id=payload.project_id, competitors=payload.competitors, **extra)


# Locations and languages

def handle_locations_and_languages(payload: LocationsAndLanguagesRequest, client: AhrefsClient):
    extra = payload.extra or {}
    return client.get_locations_and_languages(**extra)


# Keyword lists

def handle_keyword_lists(payload: KeywordListsRequest, client: AhrefsClient):
    extra = payload.extra or {}
    if payload.project_id:
        extra = dict(extra or {})
        extra.setdefault("project_id", payload.project_id)
    return client.get_keyword_lists(**(extra or {}))
