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
    
    def get_term(self):
        return self.term

term_manager = ElectionTerm()
leader_is_me = None

def try_fetch_leader(tcp_address):
    leader = coord.get("leader")
    if leader is None:
        propose_vote(tcp_address)

def propose_vote(tcp_address):
    success = coord.set("leader", tcp_address)
    leader_is_me = success
    if leader_is_me:
        term_manager.new_term()

def check_leader_validity(leader_term):
    leader_validity_flag = True
    try:
        term_manager.compare_terms(leader_term)
    except:
        leader_validity_flag = False
    
    return leader_validity_flag
