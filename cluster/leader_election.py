import manager as coord

class ElectionTerm:
    def __init__(self):
        self.term = 0
    
    def new_term(self):
        self.term += 1
    
    def compare_terms(self, remote_leader_term):
        if remote_leader_term < self.term:
            # split brain occured
            raise "Split Brain! Notice the old leader"
        
        # merge the term 
        if remote_leader_term > self.term:
            self.term = remote_leader_term


def start_leader_election():
    pass

async def wait_for_heartbeat():
    pass
