from models import personality, twitter, base
from .ext import db

schemas = {"twitter", "personality"}
required = {"twitter": ["id", "follows"], "personality": ["personality", "document"]}
document_model = {"twitter": twitter.Document, "personality": personality.Document}
user_model = {"twitter": twitter.User, "personality": personality.User}
#! features = base.WORDF_TYPES
features = ["HGI_positiv", "HGI_negativ", "HGI_pstv", "HGI_affil", "HGI_ngtv", "HGI_hostile", "HGI_strong", "HGI_power", "HGI_weak", "HGI_submit", "HGI_active", "HGI_passive", "HGI_pleasur", "HGI_pain", "HGI_feel", "HGI_arousal", "HGI_emot", "HGI_virtue", "HGI_vice", "HGI_ovrst", "HGI_undrst", "HGI_academ", "HGI_doctrin", "HGI_econ2", "HGI_exch", "HGI_econ", "HGI_exprsv", "HGI_legal", "HGI_milit", "HGI_polit2", "HGI_polit", "HGI_relig", "HGI_role", "HGI_coll", "HGI_work", "HGI_ritual", "HGI_socrel", "HGI_race", "HGI_kin2", "HGI_male", "HGI_female", "HGI_nonadlt", "HGI_hu", "HGI_ani", "HGI_place", "HGI_social", "HGI_region", "HGI_route", "HGI_aquatic", "HGI_land", "HGI_sky", "HGI_object", "HGI_tool", "HGI_food", "HGI_vehicle", "HGI_bldgpt", "HGI_comnobj", "HGI_natobj", "HGI_bodypt", "HGI_comform", "HGI_com", "HGI_say", "HGI_need", "HGI_goal", "HGI_try", "HGI_means", "HGI_persist", "HGI_complet", "HGI_fail", "HGI_natrpro", "HGI_begin", "HGI_vary", "HGI_increas", "HGI_decreas", "HGI_finish", "HGI_stay", "HGI_rise", "HGI_exert", "HGI_fetch", "HGI_travel", "HGI_fall", "HGI_think", "HGI_know", "HGI_causal", "HGI_ought", "HGI_perceiv", "HGI_compare", "HGI_eval2", "HGI_eval", "HGI_solve", "HGI_abs2", "HGI_abs", "HGI_quality", "HGI_quan", "HGI_numb", "HGI_ord", "HGI_card", "HGI_freq", "HGI_dist", "HGI_time2", "HGI_time", "HGI_space", "HGI_pos", "HGI_dim", "HGI_rel", "HGI_color", "HGI_self", "HGI_our", "HGI_you", "HGI_name", "HGI_yes", "HGI_no", "HGI_negate", "HGI_intrj", "HGI_iav", "HGI_dav", "HGI_sv", "HGI_ipadj", "HGI_indadj", "HGI_powgain", "HGI_powloss", "HGI_powends", "HGI_powaren", "HGI_powcon", "HGI_powcoop", "HGI_powaupt", "HGI_powpt", "HGI_powdoct", "HGI_powauth", "HGI_powoth", "HGI_powtot", "HGI_rcethic", "HGI_rcrelig", "HGI_rcgain", "HGI_rcloss", "HGI_rcends", "HGI_rctot", "HGI_rspgain", "HGI_rsploss", "HGI_rspoth", "HGI_rsptot", "HGI_affgain", "HGI_affloss", "HGI_affpt", "HGI_affoth", "HGI_afftot", "HGI_wltpt", "HGI_wlttran", "HGI_wltoth", "HGI_wlttot", "HGI_wlbgain", "HGI_wlbloss", "HGI_wlbphys", "HGI_wlbpsyc", "HGI_wlbpt", "HGI_wlbtot", "HGI_enlgain", "HGI_enlloss", "HGI_enlends", "HGI_enlpt", "HGI_enloth", "HGI_enltot", "HGI_sklasth", "HGI_sklpt", "HGI_skloth", "HGI_skltot", "HGI_trngain", "HGI_trnloss", "HGI_tranlw", "HGI_meanslw", "HGI_endslw", "HGI_arenalw", "HGI_ptlw", "HGI_nation", "HGI_anomie", "HGI_negaff", "HGI_posaff", "HGI_surelw", "HGI_if", "HGI_notlw", "HGI_timespc", "HGI_formlw", "LIWC_function", "LIWC_pronoun", "LIWC_ppron", "LIWC_i", "LIWC_we", "LIWC_you", "LIWC_shehe", "LIWC_they", "LIWC_ipron", "LIWC_article", "LIWC_prep", "LIWC_auxverb", "LIWC_adverb", "LIWC_conj", "LIWC_negate", "LIWC_verb", "LIWC_adj", "LIWC_compare", "LIWC_interrog", "LIWC_number", "LIWC_quant", "LIWC_affect", "LIWC_posemo", "LIWC_negemo", "LIWC_anx", "LIWC_anger", "LIWC_sad", "LIWC_social", "LIWC_family", "LIWC_friend", "LIWC_female", "LIWC_male", "LIWC_cogproc", "LIWC_insight", "LIWC_cause", "LIWC_discrep", "LIWC_tentat", "LIWC_certain", "LIWC_differ", "LIWC_percept", "LIWC_see", "LIWC_hear", "LIWC_feel", "LIWC_bio", "LIWC_body", "LIWC_health", "LIWC_sexual", "LIWC_ingest", "LIWC_drives", "LIWC_affiliation", "LIWC_achiev", "LIWC_power", "LIWC_reward", "LIWC_risk", "LIWC_focuspast", "LIWC_focuspresent", "LIWC_focusfuture", "LIWC_relativ", "LIWC_motion", "LIWC_space", "LIWC_time", "LIWC_work", "LIWC_leisure", "LIWC_home", "LIWC_money", "LIWC_relig", "LIWC_death", "LIWC_informal", "LIWC_swear", "LIWC_netspeak", "LIWC_assent", "LIWC_nonflu", "LIWC_filler", "MRC_kf_freq", "MRC_kf_nsamp", "MRC_tl_freq", "MRC_brown_freq", "MRC_fam", "MRC_conc", "MRC_imag", "MRC_meanc", "MRC_meanp", "MRC_aoa", "NRC_positive", "NRC_negative", "NRC_anger", "NRC_anticipation", "NRC_disgust", "NRC_fear", "NRC_joy", "NRC_sadness", "NRC_surprise", "NRC_trust", "S_visual", "S_auditory", "S_gustatory", "S_olfactory", "S_tactile"]
    

def message(m, s="success"):
    return {"state" : s, "message": m}

def json(id, schema):
    user = user_model[schema].query.get_or_404(id)
    document = document_model[schema].query.get_or_404(id)
    
    response = {
        "_id": id,
        "user": user.json,
        "document" : document.json
    }
    return response