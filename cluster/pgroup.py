import manager as coord

def add_node(address):
    coord.append("cluster", address)

def register_seed(address):
    return coord.set("seed", address)

def retrieve_seed():
    return coord.get("seed")

def get_cluster_nodes():
    return coord.fetch_all("cluster")

def get_cluster_len():
    return coord.count_items("cluster")

def delete_node(peer):
    return coord.delete_item("cluster", peer)

def search_leader():
    return coord.get("leader")

def propose_vote(addr):
    return coord.set("leader", addr)
