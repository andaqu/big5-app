from collections import Counter
from sqlalchemy import func
from app.ext import db
import numpy as np

class BaseDocument(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text())
    features = db.Column(db.ARRAY(db.Float()))

    def __init__(self, text):
        self.text = text

    @property
    def json(self):
        return {
            "text": self.text,
            "features": self.features
        }


    def compute_features(self):
        # Duplicate every apostrophe: this is for PostgreSQL, since apostrophe's are escaped by themselves
        text = self.text.replace("'", "''")

        # Split the text into words and get the document's count for every word
        words = text.split(" ")
        count = Counter(words)
        vocab = list(count.keys())

        total = np.zeros(FEATURES)
        sub = np.zeros(FEATURES)

        # Set up query input: ["Hello", "world"] => '{"Hello", "world"}'
        q = '{"' + '", "'.join(vocab) + '"}'

        # Get word features and convert to dictionary
        wordfs = db.session.execute(f"SELECT * FROM match_words('{q}');").fetchall() #! approx 0.2second/1k words
        wordfs = {x[0]: x[1:] for x in wordfs}

        for word in wordfs:

            wordf = wordfs[word]

            # Convert wordf into a numpy array called new
            new = np.array(wordf, dtype=float) 

            # Keep track of zero-valued continuous features
            sub += ((FLOATS == True) & np.isnan(new)) * count[word]

            # Aggregate feature values within total
            total += np.nan_to_num(new, 0) * count[word]

        # set(count) - set(wordfs) is the set of words in the document not in the Words table
        for word in set(count) - set(wordfs):
            sub += (FLOATS == True) * count[word]

        # For categoricals: calculate the average, and thus probability of words belonging to a given category, by total / |D|
        # For continuous values: calculate the non-zero average (this is why `sub` is needed!)
        # It can be the case that len(words) = sub, that is to say a division by 0 may be imminent.
        # This happens when a continuous value is always None for a given document. We don't really care for this and we can just ignore it.
        # If this were to happen though, make sure to convert them to 0.
        with np.errstate(divide='ignore',invalid='ignore'):
            total = total / (len(words) - sub).astype('float')
            total = np.nan_to_num(total, 0)

        total = total.tolist()

        # average word length is a last-second feature, deal with double apostrophe
        # avg_word_len = (sum(map(len, words)) - text.count("''")) / float(len(words)) 
        # total.append(avg_word_len)

        self.features = total

        return self.features
 
class BaseUser(db.Model):
    __abstract__ = True

    @property
    def json(self):
        return {"personality": { "o": self.o, "c": self.c, "e": self.e, "a": self.a, "n": self.n }}

    id = db.Column(db.Integer, primary_key=True)
    o = db.Column(db.Float())
    c = db.Column(db.Float())
    e = db.Column(db.Float())
    a = db.Column(db.Float())
    n = db.Column(db.Float())

class Word(db.Model):
    __table_args__ = {'schema': "public"}
    __tablename__ = "Word"

    word = db.Column(db.String, primary_key=True)
    HGI_positiv = db.Column(db.Integer())
    HGI_negativ = db.Column(db.Integer())
    HGI_pstv = db.Column(db.Integer())
    HGI_affil = db.Column(db.Integer())
    HGI_ngtv = db.Column(db.Integer())
    HGI_hostile = db.Column(db.Integer())
    HGI_strong = db.Column(db.Integer())
    HGI_power = db.Column(db.Integer())
    HGI_weak = db.Column(db.Integer())
    HGI_submit = db.Column(db.Integer())
    HGI_active = db.Column(db.Integer())
    HGI_passive = db.Column(db.Integer())
    HGI_pleasur = db.Column(db.Integer())
    HGI_pain = db.Column(db.Integer())
    HGI_feel = db.Column(db.Integer())
    HGI_arousal = db.Column(db.Integer())
    HGI_emot = db.Column(db.Integer())
    HGI_virtue = db.Column(db.Integer())
    HGI_vice = db.Column(db.Integer())
    HGI_ovrst = db.Column(db.Integer())
    HGI_undrst = db.Column(db.Integer())
    HGI_academ = db.Column(db.Integer())
    HGI_doctrin = db.Column(db.Integer())
    HGI_econ2 = db.Column(db.Integer())
    HGI_exch = db.Column(db.Integer())
    HGI_econ = db.Column(db.Integer())
    HGI_exprsv = db.Column(db.Integer())
    HGI_legal = db.Column(db.Integer())
    HGI_milit = db.Column(db.Integer())
    HGI_polit2 = db.Column(db.Integer())
    HGI_polit = db.Column(db.Integer())
    HGI_relig = db.Column(db.Integer())
    HGI_role = db.Column(db.Integer())
    HGI_coll = db.Column(db.Integer())
    HGI_work = db.Column(db.Integer())
    HGI_ritual = db.Column(db.Integer())
    HGI_socrel = db.Column(db.Integer())
    HGI_race = db.Column(db.Integer())
    HGI_kin2 = db.Column(db.Integer())
    HGI_male = db.Column(db.Integer())
    HGI_female = db.Column(db.Integer())
    HGI_nonadlt = db.Column(db.Integer())
    HGI_hu = db.Column(db.Integer())
    HGI_ani = db.Column(db.Integer())
    HGI_place = db.Column(db.Integer())
    HGI_social = db.Column(db.Integer())
    HGI_region = db.Column(db.Integer())
    HGI_route = db.Column(db.Integer())
    HGI_aquatic = db.Column(db.Integer())
    HGI_land = db.Column(db.Integer())
    HGI_sky = db.Column(db.Integer())
    HGI_object = db.Column(db.Integer())
    HGI_tool = db.Column(db.Integer())
    HGI_food = db.Column(db.Integer())
    HGI_vehicle = db.Column(db.Integer())
    HGI_bldgpt = db.Column(db.Integer())
    HGI_comnobj = db.Column(db.Integer())
    HGI_natobj = db.Column(db.Integer())
    HGI_bodypt = db.Column(db.Integer())
    HGI_comform = db.Column(db.Integer())
    HGI_com = db.Column(db.Integer())
    HGI_say = db.Column(db.Integer())
    HGI_need = db.Column(db.Integer())
    HGI_goal = db.Column(db.Integer())
    HGI_try = db.Column(db.Integer())
    HGI_means = db.Column(db.Integer())
    HGI_persist = db.Column(db.Integer())
    HGI_complet = db.Column(db.Integer())
    HGI_fail = db.Column(db.Integer())
    HGI_natrpro = db.Column(db.Integer())
    HGI_begin = db.Column(db.Integer())
    HGI_vary = db.Column(db.Integer())
    HGI_increas = db.Column(db.Integer())
    HGI_decreas = db.Column(db.Integer())
    HGI_finish = db.Column(db.Integer())
    HGI_stay = db.Column(db.Integer())
    HGI_rise = db.Column(db.Integer())
    HGI_exert = db.Column(db.Integer())
    HGI_fetch = db.Column(db.Integer())
    HGI_travel = db.Column(db.Integer())
    HGI_fall = db.Column(db.Integer())
    HGI_think = db.Column(db.Integer())
    HGI_know = db.Column(db.Integer())
    HGI_causal = db.Column(db.Integer())
    HGI_ought = db.Column(db.Integer())
    HGI_perceiv = db.Column(db.Integer())
    HGI_compare = db.Column(db.Integer())
    HGI_eval2 = db.Column(db.Integer())
    HGI_eval = db.Column(db.Integer())
    HGI_solve = db.Column(db.Integer())
    HGI_abs2 = db.Column(db.Integer())
    HGI_abs = db.Column(db.Integer())
    HGI_quality = db.Column(db.Integer())
    HGI_quan = db.Column(db.Integer())
    HGI_numb = db.Column(db.Integer())
    HGI_ord = db.Column(db.Integer())
    HGI_card = db.Column(db.Integer())
    HGI_freq = db.Column(db.Integer())
    HGI_dist = db.Column(db.Integer())
    HGI_time2 = db.Column(db.Integer())
    HGI_time = db.Column(db.Integer())
    HGI_space = db.Column(db.Integer())
    HGI_pos = db.Column(db.Integer())
    HGI_dim = db.Column(db.Integer())
    HGI_rel = db.Column(db.Integer())
    HGI_color = db.Column(db.Integer())
    HGI_self = db.Column(db.Integer())
    HGI_our = db.Column(db.Integer())
    HGI_you = db.Column(db.Integer())
    HGI_name = db.Column(db.Integer())
    HGI_yes = db.Column(db.Integer())
    HGI_no = db.Column(db.Integer())
    HGI_negate = db.Column(db.Integer())
    HGI_intrj = db.Column(db.Integer())
    HGI_iav = db.Column(db.Integer())
    HGI_dav = db.Column(db.Integer())
    HGI_sv = db.Column(db.Integer())
    HGI_ipadj = db.Column(db.Integer())
    HGI_indadj = db.Column(db.Integer())
    HGI_powgain = db.Column(db.Integer())
    HGI_powloss = db.Column(db.Integer())
    HGI_powends = db.Column(db.Integer())
    HGI_powaren = db.Column(db.Integer())
    HGI_powcon = db.Column(db.Integer())
    HGI_powcoop = db.Column(db.Integer())
    HGI_powaupt = db.Column(db.Integer())
    HGI_powpt = db.Column(db.Integer())
    HGI_powdoct = db.Column(db.Integer())
    HGI_powauth = db.Column(db.Integer())
    HGI_powoth = db.Column(db.Integer())
    HGI_powtot = db.Column(db.Integer())
    HGI_rcethic = db.Column(db.Integer())
    HGI_rcrelig = db.Column(db.Integer())
    HGI_rcgain = db.Column(db.Integer())
    HGI_rcloss = db.Column(db.Integer())
    HGI_rcends = db.Column(db.Integer())
    HGI_rctot = db.Column(db.Integer())
    HGI_rspgain = db.Column(db.Integer())
    HGI_rsploss = db.Column(db.Integer())
    HGI_rspoth = db.Column(db.Integer())
    HGI_rsptot = db.Column(db.Integer())
    HGI_affgain = db.Column(db.Integer())
    HGI_affloss = db.Column(db.Integer())
    HGI_affpt = db.Column(db.Integer())
    HGI_affoth = db.Column(db.Integer())
    HGI_afftot = db.Column(db.Integer())
    HGI_wltpt = db.Column(db.Integer())
    HGI_wlttran = db.Column(db.Integer())
    HGI_wltoth = db.Column(db.Integer())
    HGI_wlttot = db.Column(db.Integer())
    HGI_wlbgain = db.Column(db.Integer())
    HGI_wlbloss = db.Column(db.Integer())
    HGI_wlbphys = db.Column(db.Integer())
    HGI_wlbpsyc = db.Column(db.Integer())
    HGI_wlbpt = db.Column(db.Integer())
    HGI_wlbtot = db.Column(db.Integer())
    HGI_enlgain = db.Column(db.Integer())
    HGI_enlloss = db.Column(db.Integer())
    HGI_enlends = db.Column(db.Integer())
    HGI_enlpt = db.Column(db.Integer())
    HGI_enloth = db.Column(db.Integer())
    HGI_enltot = db.Column(db.Integer())
    HGI_sklasth = db.Column(db.Integer())
    HGI_sklpt = db.Column(db.Integer())
    HGI_skloth = db.Column(db.Integer())
    HGI_skltot = db.Column(db.Integer())
    HGI_trngain = db.Column(db.Integer())
    HGI_trnloss = db.Column(db.Integer())
    HGI_tranlw = db.Column(db.Integer())
    HGI_meanslw = db.Column(db.Integer())
    HGI_endslw = db.Column(db.Integer())
    HGI_arenalw = db.Column(db.Integer())
    HGI_ptlw = db.Column(db.Integer())
    HGI_nation = db.Column(db.Integer())
    HGI_anomie = db.Column(db.Integer())
    HGI_negaff = db.Column(db.Integer())
    HGI_posaff = db.Column(db.Integer())
    HGI_surelw = db.Column(db.Integer())
    HGI_if = db.Column(db.Integer())
    HGI_notlw = db.Column(db.Integer())
    HGI_timespc = db.Column(db.Integer())
    HGI_formlw = db.Column(db.Integer())
    LIWC_function = db.Column(db.Integer())
    LIWC_pronoun = db.Column(db.Integer())
    LIWC_ppron = db.Column(db.Integer())
    LIWC_i = db.Column(db.Integer())
    LIWC_we = db.Column(db.Integer())
    LIWC_you = db.Column(db.Integer())
    LIWC_shehe = db.Column(db.Integer())
    LIWC_they = db.Column(db.Integer())
    LIWC_ipron = db.Column(db.Integer())
    LIWC_article = db.Column(db.Integer())
    LIWC_prep = db.Column(db.Integer())
    LIWC_auxverb = db.Column(db.Integer())
    LIWC_adverb = db.Column(db.Integer())
    LIWC_conj = db.Column(db.Integer())
    LIWC_negate = db.Column(db.Integer())
    LIWC_verb = db.Column(db.Integer())
    LIWC_adj = db.Column(db.Integer())
    LIWC_compare = db.Column(db.Integer())
    LIWC_interrog = db.Column(db.Integer())
    LIWC_number = db.Column(db.Integer())
    LIWC_quant = db.Column(db.Integer())
    LIWC_affect = db.Column(db.Integer())
    LIWC_posemo = db.Column(db.Integer())
    LIWC_negemo = db.Column(db.Integer())
    LIWC_anx = db.Column(db.Integer())
    LIWC_anger = db.Column(db.Integer())
    LIWC_sad = db.Column(db.Integer())
    LIWC_social = db.Column(db.Integer())
    LIWC_family = db.Column(db.Integer())
    LIWC_friend = db.Column(db.Integer())
    LIWC_female = db.Column(db.Integer())
    LIWC_male = db.Column(db.Integer())
    LIWC_cogproc = db.Column(db.Integer())
    LIWC_insight = db.Column(db.Integer())
    LIWC_cause = db.Column(db.Integer())
    LIWC_discrep = db.Column(db.Integer())
    LIWC_tentat = db.Column(db.Integer())
    LIWC_certain = db.Column(db.Integer())
    LIWC_differ = db.Column(db.Integer())
    LIWC_percept = db.Column(db.Integer())
    LIWC_see = db.Column(db.Integer())
    LIWC_hear = db.Column(db.Integer())
    LIWC_feel = db.Column(db.Integer())
    LIWC_bio = db.Column(db.Integer())
    LIWC_body = db.Column(db.Integer())
    LIWC_health = db.Column(db.Integer())
    LIWC_sexual = db.Column(db.Integer())
    LIWC_ingest = db.Column(db.Integer())
    LIWC_drives = db.Column(db.Integer())
    LIWC_affiliation = db.Column(db.Integer())
    LIWC_achiev = db.Column(db.Integer())
    LIWC_power = db.Column(db.Integer())
    LIWC_reward = db.Column(db.Integer())
    LIWC_risk = db.Column(db.Integer())
    LIWC_focuspast = db.Column(db.Integer())
    LIWC_focuspresent = db.Column(db.Integer())
    LIWC_focusfuture = db.Column(db.Integer())
    LIWC_relativ = db.Column(db.Integer())
    LIWC_motion = db.Column(db.Integer())
    LIWC_space = db.Column(db.Integer())
    LIWC_time = db.Column(db.Integer())
    LIWC_work = db.Column(db.Integer())
    LIWC_leisure = db.Column(db.Integer())
    LIWC_home = db.Column(db.Integer())
    LIWC_money = db.Column(db.Integer())
    LIWC_relig = db.Column(db.Integer())
    LIWC_death = db.Column(db.Integer())
    LIWC_informal = db.Column(db.Integer())
    LIWC_swear = db.Column(db.Integer())
    LIWC_netspeak = db.Column(db.Integer())
    LIWC_assent = db.Column(db.Integer())
    LIWC_nonflu = db.Column(db.Integer())
    LIWC_filler = db.Column(db.Integer())
    MRC_kf_freq = db.Column(db.Float())
    MRC_kf_nsamp = db.Column(db.Float())
    MRC_tl_freq = db.Column(db.Float())
    MRC_brown_freq = db.Column(db.Float())
    MRC_fam = db.Column(db.Float())
    MRC_conc = db.Column(db.Float())
    MRC_imag = db.Column(db.Float())
    MRC_meanc = db.Column(db.Float())
    MRC_meanp = db.Column(db.Float())
    MRC_aoa = db.Column(db.Float())
    NRC_positive = db.Column(db.Integer())
    NRC_negative = db.Column(db.Integer())
    NRC_anger = db.Column(db.Integer())
    NRC_anticipation = db.Column(db.Integer())
    NRC_disgust = db.Column(db.Integer())
    NRC_fear = db.Column(db.Integer())
    NRC_joy = db.Column(db.Integer())
    NRC_sadness = db.Column(db.Integer())
    NRC_surprise = db.Column(db.Integer())
    NRC_trust = db.Column(db.Integer())
    S_visual = db.Column(db.Float())
    S_auditory = db.Column(db.Float())
    S_gustatory = db.Column(db.Float())
    S_olfactory = db.Column(db.Float())
    S_tactile = db.Column(db.Float())

# The first type is ignored since it is the word itself (String)
WORDF_TYPES = [column.type for column in Word.__table__.columns][1:]
FEATURES = len(WORDF_TYPES)
FLOATS = np.array([True if str(t) is "FLOAT" else False for t in WORDF_TYPES])