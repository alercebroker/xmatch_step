ALLWISE_KEYS = [
    "oid_catalog",
    "ra",
    "dec",
    "w1mpro",
    "w2mpro",
    "w3mpro",
    "w4mpro",
    "w1sigmpro",
    "w2sigmpro",
    "w3sigmpro",
    "w4sigmpro",
    "j_m_2mass",
    "h_m_2mass",
    "k_m_2mass",
    "j_msig_2mass",
    "h_msig_2mass",
    "k_msig_2mass",
]

XMATCH_KEYS = ["oid", "catid", "oid_catalog", "dist", "class_catalog", "period"]

# Temporal code: the oid in oid_in will replace with aid_in
ALLWISE_MAP = {
    "AllWISE": "oid_catalog",
    "RAJ2000": "ra",
    "DECJ2000": "dec",
    "W1mag": "w1mpro",
    "W2mag": "w2mpro",
    "W3mag": "w3mpro",
    "W4mag": "w4mpro",
    "e_W1mag": "w1sigmpro",
    "e_W2mag": "w2sigmpro",
    "e_W3mag": "w3sigmpro",
    "e_W4mag": "w4sigmpro",
    "Jmag": "j_m_2mass",
    "Hmag": "h_m_2mass",
    "Kmag": "k_m_2mass",
    "e_Jmag": "j_msig_2mass",
    "e_Hmag": "h_msig_2mass",
    "e_Kmag": "k_msig_2mass",
    "oid_in": "oid",
    "angDist": "dist",
}
