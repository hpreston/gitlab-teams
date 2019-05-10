import os

def event_handler(msg):
    """
    receives gitlab message and executes the appropriate formatter
    """

    if os.getenv("DEBUG"):
        print(msg)

    handler_map = {
        'push': push_formatter,
        'issue': issue_formatter,
        'pipeline': pipeline_formatter,
        'note': note_formatter,
        'build': builds_formatter,
        'merge_request': merge_request_formatter
    }

    object_kind = msg['object_kind']
    message = handler_map[object_kind](msg)
    return message


def push_formatter(msg):
    message = "In [{}]({}), {} pushed just pushed commit(s)\n".format(msg['project']['path_with_namespace'],
                                                                    msg['project']['git_http_url'],
                                                                    msg['user_name'])
    for commit in msg['commits']:
        message += "* [{}]({})\n".format(commit['message'], commit['url'])
    return message

def issue_formatter(msg):
    issue = msg['object_attributes']
    message = "In [{}]({}), {} just {} an issue.\n".format(msg['project']['path_with_namespace'],
                                                         msg['project']['git_http_url'],
                                                         msg['user']['username'],
                                                         issue['state'])

    message += "* [{}]({})\n".format(issue['title'], issue['url'])
    if msg['labels']:
        message += " : Labels: "
        for l in msg['labels']:
            message += "{} ".format(l['title'])

    return message

def pipeline_formatter(msg):
    # repo = msg['project']['path_with_namespace']
    # url = msg['project']['web_url'] + '/pipelines'
    # return "Pipeline Event occurred in [{}]({})".format(repo, url)
    repo_name = msg['project']['path_with_namespace']
    repo_url = msg['project']['web_url']
    pipeline_id = msg['object_attributes']['id']
    pipeline_url = repo_url + '/pipelines/{}'.format(pipeline_id)
    commit_msg = msg['commit']['message']
    commit_url = msg['commit']['url']

    sparkmsg = "## Pipeline update for [#{0}]({1})"
    sparkmsg += "\n\n[{2}]({3})"
    sparkmsg += "\n\n### Build Job Status"

    sparkmsg = sparkmsg.format(pipeline_id, pipeline_url, commit_msg, commit_url)

    for build in msg['builds']:
        sparkmsg += "\n\n* **{}:** {}".format(build['name'], build['status'])

    return sparkmsg

def note_formatter(msg):
    repo_url = msg['project']['web_url']
    repo = msg['project']['path_with_namespace']
    note = msg['object_attributes']['note']
    note_url = msg['object_attributes']['url']
    user = msg['user']['username']

    sparkmsg = ""
    sparkmsg += "**{} just created a new [note]({}) in {}:**".format(user, note_url, repo)
    sparkmsg += "\n\n{}".format(note)

    return sparkmsg

def builds_formatter(msg):
    build = msg
    status = build['build_status']
    build_id = build['build_id']
    stage = build['build_stage']
    repo = build['project_name']
    commit_msg = build['commit']['message']
    repo_url = build['repository']['homepage'] + '/pipelines'
    sparkmsg = ""
    sparkmsg += "## Build update for build {}\n".format(build_id)
    sparkmsg += "\n\n**Repostory**: [{}]({})".format(repo, repo_url)
    sparkmsg += "\n\n**Status**: {}".format(status)
    sparkmsg += "\n\n**Stage**: {}".format(stage)
    sparkmsg += "\n\n**Commit Message**: {}".format(commit_msg)

    # we may be covered in pipeline events
    # return sparkmsg
    return None

def merge_request_formatter(msg):
    # glean important information from incoming message
    mr = msg['object_attributes']
    source_branch = mr['source_branch']
    target_branch = mr['target_branch']
    user = msg['user']['username']
    source_repo = mr['source']['path_with_namespace']
    target_repo = mr['target']['path_with_namespace']
    target_repo_url = mr['target']['homepage']
    state = mr['state']
    title = mr['title']
    merge_id = mr['iid']
    url = mr['url']
    target_repo = "[{}]({})".format(target_repo, target_repo_url)
    # format spark message
    message = ""
    message += "### In {}.  ".format(target_repo)
    message += "[merge request #{}]({}) was {} by {}".format(merge_id, url, state, user)
    return message
