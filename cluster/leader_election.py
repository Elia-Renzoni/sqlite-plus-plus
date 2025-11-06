from . import pgroup as pg

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
    
    def get_term(self):
        return self.term

term_manager = ElectionTerm()
leader_is_me = None

def fetch_leader():
    return pg.search_leader()

def try_fetch_leader(tcp_address):
    leader = pg.search_leader()
    if leader is None:
        propose_vote(tcp_address)

def propose_vote(tcp_address):
    success = pg.propose_vote(tcp_address)
    leader_is_me = success
    if leader_is_me:
        term_manager.new_term()

def change_status_as_peer():
    leader_is_me = False

def fetch_leader_status():
    return leader_is_me

def check_leader_validity(leader_term):
    leader_validity_flag = True
    try:
        term_manager.compare_terms(leader_term)
    except:
        leader_validity_flag = False
    
    return leader_validity_flag
