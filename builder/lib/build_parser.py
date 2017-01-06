
class BuildParser:

    def __init__(self, record):
        self.date_created = record['date_created']['S']
        self.date_modified = record['date_modified']['S']
        self.id = record['id']['S']
        self.event_type = record['event_type']['S']
        self.logs = record['logs']['S']
        self.repo_id = record['repo_id']['S']
        self.repo_name = record['repo_name']['S']
        self.repo_owner = record['repo_owner']['S']
        self.sha = record['sha']['S']
        self.tag = record['tag']['S']
