from django import forms
from gradpro.models import User, SelfManagement, SocialIntelligence, Innovation, Communication, Adaptability


class UserForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())
    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')

# Forms for the general meta-skills test (3 in total, 1 for each meta-skill)
class SelfManagementForm(forms.ModelForm):
    # Concentration
    # The available choices
    c_CHOICES = (
        (1, 'Strongly disagree '),
        (2, 'Disagree'),
        (3, 'Somewhat disagree '),
        (4, 'Neither agree nor disagree '),
        (5, 'Somewhat agree '),
        (6, 'Agree'),
        (7, 'Strongly agree '),
    )

    # The labels for the questions
    c_l1 = "I find it easy to meet deadlines"
    c_l2 = "I find it easy to prioritise tasks"
    c_l3 = "I find it easy to stay on task"

    c_q1 = forms.ChoiceField(label=c_l1, required=True, choices=c_CHOICES,
                             widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    c_q2 = forms.ChoiceField(label=c_l2, required=True, choices=c_CHOICES,
                             widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    c_q3 = forms.ChoiceField(label=c_l3, required=True, choices=c_CHOICES,
                             widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))

    # Adaptability
    a_CHOICES = (
        (1, 'You are pleased to hear about the  innovation and try the new technique  '),
        (2, 'You investigate the technique to see how relevant it is to your project  '),
        (3, 'You decide that you are committed to your own techniques and continue your original plan  ')
    )

    a_l1 = "Imagine you have been working on a project for the past two months and the client is expecting it to be " \
           "finished soon.  A colleague highlights a new technique that will simplify the project. " \
           "What is your reaction to this?"
    a_q1 = forms.ChoiceField(label=a_l1, required=True, choices=a_CHOICES,
                             widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))

    # Initiative
    i_CHOICES = (
        (1, 'Strongly disagree '),
        (2, 'Disagree'),
        (3, 'Somewhat disagree '),
        (4, 'Neither agree nor disagree '),
        (5, 'Somewhat agree '),
        (6, 'Agree'),
        (7, 'Strongly agree '),
    )

    i_l1 = "I feel confident sharing my ideas"
    i_l2 = "I feel confident in producing new concepts "
    i_l3 = "I am confident in my own abilities "
    i_l4 = "I am comfortable taking calculated risks in my work "

    i_q1 = forms.ChoiceField(label=i_l1, required=True, choices=i_CHOICES,
                             widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    i_q2 = forms.ChoiceField(label=i_l2, required=True, choices=i_CHOICES,
                             widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    i_q3 = forms.ChoiceField(label=i_l3, required=True, choices=i_CHOICES,
                             widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    i_q4 = forms.ChoiceField(label=i_l4, required=True, choices=i_CHOICES,
                             widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))

    class Meta:
        model = SelfManagement
        fields = ('c_q1', 'c_q2', 'c_q3', 'a_q1', 'i_q1', 'i_q2', 'i_q3', 'i_q4',)


class SocialIntelligenceForm(forms.ModelForm):
    # Communication
    com_CHOICES = (
        (1, 'Never confident'),
        (2, 'Sometimes confident'),
        (3, 'Often Confident'),
    )

    com_l1 = "Receiving information"
    com_l2 = "Listening "
    com_l3 = "Giving information"
    com_l4 = "Telling a story "

    com_q1 = forms.ChoiceField(label=com_l1, required=True, choices=com_CHOICES,
                               widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    com_q2 = forms.ChoiceField(label=com_l2, required=True, choices=com_CHOICES,
                               widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    com_q3 = forms.ChoiceField(label=com_l3, required=True, choices=com_CHOICES,
                               widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    com_q4 = forms.ChoiceField(label=com_l4, required=True, choices=com_CHOICES,
                               widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))

    # Collaborating
    col_CHOICES = (
        (1, 'Dislike'),
        (2, 'Neutral'),
        (3, 'Like'),
    )

    col_l1 = "Relationship building - The ability to identify and initiate connections and to develop and " \
             "maintain them in a way that is of mutual" \
             "benefit to both one's self and others"
    col_l2 = "Teamworking and collaboration - Working with others toward shared goals. Creating group synergy " \
             "in pursuing collective goals"
    col_l3 = "Social perceptiveness - Being aware of others' reactions and understanding why they react as they do"
    col_l4 = "Global and cross cultural competence - The ability to operate in different cultural settings "

    col_q1 = forms.ChoiceField(label=col_l1, required=True, choices=col_CHOICES,
                               widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    col_q2 = forms.ChoiceField(label=col_l2, required=True, choices=col_CHOICES,
                               widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    col_q3 = forms.ChoiceField(label=col_l3, required=True, choices=col_CHOICES,
                               widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    col_q4 = forms.ChoiceField(label=col_l4, required=True, choices=col_CHOICES,
                               widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))

    # Feeling
    f_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    )

    f_l1 = "Rate your confidence in employing empathy in the workplace with 1 being not confident and 10 being " \
           "very confident."
    f_q1 = forms.ChoiceField(label=f_l1, required=True, choices=f_CHOICES,
                             widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))

    class Meta:
        model = SocialIntelligence
        fields = ('com_q1', 'com_q2', 'com_q3', 'com_q4', 'col_q1', 'col_q2', 'col_q3', 'col_q4', 'f_q1')


class InnovationForm(forms.ModelForm):
    # Sense-Making
    s_CHOICES = (
        (1, 'Dislike'),
        (2, 'Neutral'),
        (3, 'Like'),
    )

    s_l1 = "Pattern recognition - The process of classifying information into objects or classes based on key features"
    s_l2 = "Holistic thinking - The ability to see the big picture and understand subtle nuances of complex situations"
    s_l3 = "Synthesis - The process of organising, manipulating. pruning and filtering gathered data into cohesive " \
           "structures for information builiding"
    s_l4 = "Opportunity - The ability to identify areas of opportunity for innovation"
    s_l5 = "Analysis - A systemic examination and evalutation of data or information. by breaking it into its " \
           "component parts to uncover their interrealationships"

    s_q1 = forms.ChoiceField(label=s_l1, required=True, choices=s_CHOICES,
                             widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    s_q2 = forms.ChoiceField(label=s_l2, required=True, choices=s_CHOICES,
                             widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    s_q3 = forms.ChoiceField(label=s_l3, required=True, choices=s_CHOICES,
                             widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    s_q4 = forms.ChoiceField(label=s_l4, required=True, choices=s_CHOICES,
                             widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    s_q5 = forms.ChoiceField(label=s_l5, required=True, choices=s_CHOICES,
                             widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))

    # Curiosity
    cu_CHOICES = (
        (1, 'Strongly disagree '),
        (2, 'Disagree'),
        (3, 'Somewhat disagree '),
        (4, 'Neither agree nor disagree '),
        (5, 'Somewhat agree '),
        (6, 'Agree'),
        (7, 'Strongly agree '),
    )

    cu_l1 = "I notice information and can reflect on whether it is significant "
    cu_l2 = "I am good at asking questions to increase my understanding "
    cu_l3 = "I have the ability to filter resources to find relevant information "
    cu_l4 = "I can recognise problems "

    cu_q1 = forms.ChoiceField(label=cu_l1, required=True, choices=cu_CHOICES,
                              widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    cu_q2 = forms.ChoiceField(label=cu_l2, required=True, choices=cu_CHOICES,
                              widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    cu_q3 = forms.ChoiceField(label=cu_l3, required=True, choices=cu_CHOICES,
                              widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    cu_q4 = forms.ChoiceField(label=cu_l4, required=True, choices=cu_CHOICES,
                              widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))

    # Creativity
    crea_CHOICES = (
        (1, 'Not confident'),
        (2, 'Somewhat Confident'),
        (3, 'Confident'),
    )

    crea_l1 = "Rate your confidence in your creativity: "
    crea_q1 = forms.ChoiceField(label=crea_l1, required=True, choices=crea_CHOICES,
                                widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))

    # Critical_Thinking
    crit_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    )

    crit_l1 = "Rate your confidence in your critical thinking skills with with 1 being not confident " \
              "and 10 being very confident."
    crit_q1 = forms.ChoiceField(label=crit_l1, required=True, choices=crit_CHOICES,
                                widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))

    class Meta:
        model = Innovation
        fields = ('s_q1', 's_q2', 's_q3', 's_q4', 's_q5', 'cu_q1', 'cu_q2', 'cu_q3', 'cu_q4', 'crea_q1', 'crit_q1')


# Forms for the communication test (6 in total, 1 for each dimension)
class SocialComposureForm(forms.ModelForm):
    CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    l1 = "I feel nervous in social situations."
    l2 = "In most social situations I feel tense and constrained."
    l3 = "When talking, my posture seems awkward and tense."
    l4 = "My voice sounds nervous when I talk with others."
    l5 = "I am relaxed when talking with others."

    q1 = forms.ChoiceField(label=l1, required=True, choices=CHOICES,
                           widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q2 = forms.ChoiceField(label=l2, required=True, choices=CHOICES,
                           widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q3 = forms.ChoiceField(label=l3, required=True, choices=CHOICES,
                           widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q4 = forms.ChoiceField(label=l4, required=True, choices=CHOICES,
                           widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q5 = forms.ChoiceField(label=l5, required=True, choices=CHOICES,
                           widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))

    class Meta:
        model = Communication
        fields = ('q1', 'q2', 'q3', 'q4', 'q5')


class SocialConfirmationForm(forms.ModelForm):
    CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    l6 = "I try to make the other person feel good."
    l7 = "I try to make the other person feel important."
    l8 = "I try to be warm when communicating with another."
    l9 = "While I'm talking I think about how the other person feels."
    l10 = "I am verbally and nonverbally supportive of other people."

    q6 = forms.ChoiceField(label=l6, required=True, choices=CHOICES,
                           widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q7 = forms.ChoiceField(label=l7, required=True, choices=CHOICES,
                           widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q8 = forms.ChoiceField(label=l8, required=True, choices=CHOICES,
                           widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q9 = forms.ChoiceField(label=l9, required=True, choices=CHOICES,
                           widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q10 = forms.ChoiceField(label=l10, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))

    class Meta:
        model = Communication
        fields = ('q6', 'q7', 'q8', 'q9', 'q10')


class SocialExperienceForm(forms.ModelForm):
    CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    l11 = "I like to be active in different social groups."
    l12 = "I enjoy socializing with various groups of people."
    l13 = "I enjoy meeting new people."
    l14 = "I find it easy to get along with new people."
    l15 = "I do not 'mix' well at social functions."

    q11 = forms.ChoiceField(label=l11, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q12 = forms.ChoiceField(label=l12, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q13 = forms.ChoiceField(label=l13, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q14 = forms.ChoiceField(label=l14, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q15 = forms.ChoiceField(label=l15, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))

    class Meta:
        model = Communication
        fields = ('q11', 'q12', 'q13', 'q14', 'q15')


class AppropriateDisclosureForm(forms.ModelForm):
    CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    l16 = "I am aware of how intimate my disclosures are."
    l17 = "I am aware of how intimate the disclosures of others are."
    l18 = "I disclosure at the same level that others disclose to me."
    l19 = "I know how appropriate my self disclosures are."
    l20 = "When I self disclosure I know what I am revealing."

    q16 = forms.ChoiceField(label=l16, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q17 = forms.ChoiceField(label=l17, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q18 = forms.ChoiceField(label=l18, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q19 = forms.ChoiceField(label=l19, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q20 = forms.ChoiceField(label=l20, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))

    class Meta:
        model = Communication
        fields = ('q16', 'q17', 'q18', 'q19', 'q20')


class ArticulationForm(forms.ModelForm):
    CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    l21 = "When speaking I have problems with grammar."
    l22 = "When speaking I have problems with grammar."
    l23 = "I sometimes use one word when I mean to use another."
    l24 = "I sometimes use words incorrectly."
    l25 = "I have difficulty pronouncing some words."

    q21 = forms.ChoiceField(label=l21, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q22 = forms.ChoiceField(label=l22, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q23 = forms.ChoiceField(label=l23, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q24 = forms.ChoiceField(label=l24, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q25 = forms.ChoiceField(label=l25, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))

    class Meta:
        model = Communication
        fields = ('q21', 'q22', 'q23', 'q24', 'q25')


class WitForm(forms.ModelForm):
    CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    l26 = "When I am anxious I often make jokes."
    l27 = "I often make jokes when in tense situations."
    l28 = "When I embarrass myself, I often make a joke about it."
    l29 = "When someone makes a negative comment about me, I respond with a witty comeback."
    l30 = "People think I am witty."

    q26 = forms.ChoiceField(label=l26, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q27 = forms.ChoiceField(label=l27, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q28 = forms.ChoiceField(label=l28, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q29 = forms.ChoiceField(label=l29, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q30 = forms.ChoiceField(label=l30, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))

    class Meta:
        model = Communication
        fields = ('q26', 'q27', 'q28', 'q29', 'q30')


# Forms for the adaptability test (five in total)
class AdaptabilityFirstForm(forms.ModelForm):
    CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    l1 = "I am able to maintain focus during emergencies"
    l2 = "I enjoy learning about cultures other than my own"
    l3 = "I usually over-react to stressful news"
    l4 = "I believe it is important to be flexible in dealing with others"
    l5 = "I take responsibility for acquiring new skills"
    l6 = "I work well with diverse others"
    l7 = "I tend to be able to read others and understand how they are feeling at any particular moment"
    l8 = "I am adept at using my body to complete relevant tasks"
    l9 = "In an emergency situation, I can put aside emotional feelings to handle important tasks"
    l10 = "I see connections between seemingly unrelated information"
    l11 = "I enjoy learning new approaches for conducting work"

    q1 = forms.ChoiceField(label=l1, required=True, choices=CHOICES,
                           widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q2 = forms.ChoiceField(label=l2, required=True, choices=CHOICES,
                           widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q3 = forms.ChoiceField(label=l3, required=True, choices=CHOICES,
                           widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q4 = forms.ChoiceField(label=l4, required=True, choices=CHOICES,
                           widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q5 = forms.ChoiceField(label=l5, required=True, choices=CHOICES,
                           widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q6 = forms.ChoiceField(label=l6, required=True, choices=CHOICES,
                           widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q7 = forms.ChoiceField(label=l7, required=True, choices=CHOICES,
                           widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q8 = forms.ChoiceField(label=l8, required=True, choices=CHOICES,
                           widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q9 = forms.ChoiceField(label=l9, required=True, choices=CHOICES,
                           widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q10 = forms.ChoiceField(label=l10, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q11 = forms.ChoiceField(label=l11, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))

    class Meta:
        model = Adaptability
        fields = ('q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10', 'q11')


class AdaptabilitySecondForm(forms.ModelForm):
    CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    l12 = "I think clearly in times of urgency"
    l13 = "I utilize my muscular strength "
    l14 = "It is important to me that I respect others’ culture"
    l15 = "I feel unequipped to deal with too much stress"
    l16 = "I am good at developing unique analyses for complex problems"
    l17 = "I am able to be objective during emergencies"
    l18 = "My insight helps me to work effectively with others"
    l19 = "I enjoy the variety and learning experiences that come from working with people of different backgrounds"
    l20 = "I can only work in an orderly environment"
    l21 = "I am easily rattled when my schedule is too full"
    l22 = "I usually step up and take action during a crisis"

    q12 = forms.ChoiceField(label=l12, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q13 = forms.ChoiceField(label=l13, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q14 = forms.ChoiceField(label=l14, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q15 = forms.ChoiceField(label=l15, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q16 = forms.ChoiceField(label=l16, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q17 = forms.ChoiceField(label=l17, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q18 = forms.ChoiceField(label=l18, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q19 = forms.ChoiceField(label=l19, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q20 = forms.ChoiceField(label=l20, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q21 = forms.ChoiceField(label=l21, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q22 = forms.ChoiceField(label=l22, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))

    class Meta:
        model = Adaptability
        fields = ('q12', 'q13', 'q14', 'q15', 'q16', 'q17', 'q18', 'q19', 'q20', 'q21', 'q22')


class AdaptabilityThirdForm(forms.ModelForm):
    CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    l23 = "I need for things to be ‘‘black and white’’"
    l24 = "I am an innovative person"
    l25 = "I feel comfortable interacting with others who have different values and customs"
    l26 = "If my environment is not comfortable (e.g., cleanliness), I cannot perform well"
    l27 = "I make excellent decisions in times of crisis"
    l28 = "I become frustrated when things are unpredictable"
    l29 = "I am able to make effective decisions without all relevant information"
    l30 = "I am an open-minded person in dealing with others"
    l31 = "I take action to improve work performance deficiencies"
    l32 = "I am usually stressed when I have a large workload"
    l33 = "I am perceptive of others and use that knowledge in interactions"

    q23 = forms.ChoiceField(label=l23, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q24 = forms.ChoiceField(label=l24, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q25 = forms.ChoiceField(label=l25, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q26 = forms.ChoiceField(label=l26, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q27 = forms.ChoiceField(label=l27, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q28 = forms.ChoiceField(label=l28, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q29 = forms.ChoiceField(label=l29, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q30 = forms.ChoiceField(label=l30, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q31 = forms.ChoiceField(label=l31, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q32 = forms.ChoiceField(label=l32, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q33 = forms.ChoiceField(label=l33, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))

    class Meta:
        model = Adaptability
        fields = ('q23', 'q24', 'q25', 'q26', 'q27', 'q28', 'q29', 'q30', 'q31', 'q32', 'q33')


class AdaptabilityFourthForm(forms.ModelForm):
    CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    l34 = "I often learn new information and skills to stay at the forefront of my profession"
    l35 = "I often cry or get angry when I am under a great deal of stress"
    l36 = "When resources are insufficient, I thrive on developing innovative solutions"
    l37 = "I am able to look at problems from a multitude of angles"
    l38 = "I quickly learn new methods to solve problems"
    l39 = "I tend to perform best in stable situations and environments"
    l40 = "When something unexpected happens, I readily change gears in response"
    l41 = "I would quit my job if it required me to be physically stronger"
    l42 = "I try to be flexible when dealing with others"
    l43 = "I can adapt to changing situations"
    l44 = "I train to keep my work skills and knowledge current"

    q34 = forms.ChoiceField(label=l34, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q35 = forms.ChoiceField(label=l35, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q36 = forms.ChoiceField(label=l36, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q37 = forms.ChoiceField(label=l37, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q38 = forms.ChoiceField(label=l38, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q39 = forms.ChoiceField(label=l39, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q40 = forms.ChoiceField(label=l40, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q41 = forms.ChoiceField(label=l41, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q42 = forms.ChoiceField(label=l42, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q43 = forms.ChoiceField(label=l43, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q44 = forms.ChoiceField(label=l44, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))

    class Meta:
        model = Adaptability
        fields = ('q34', 'q35', 'q36', 'q37', 'q38', 'q39', 'q40', 'q41', 'q42', 'q43', 'q44')


class AdaptabilityFifthForm(forms.ModelForm):
    CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    l45 = "I physically push myself to complete important tasks"
    l46 = "I am continually learning new skills for my job"
    l47 = "I perform well in uncertain situations"
    l48 = "I can work effectively even when I am tired"
    l49 = "I take responsibility for staying current in my profession"
    l50 = "I adapt my behavior to get along with others"
    l51 = "I cannot work well if it is too hot or cold"
    l52 = "I easily respond to changing conditions"
    l53 = "I try to learn new skills for my job before they are needed"
    l54 = "I can adjust my plans to changing conditions"
    l55 = "I keep working even when I am physically exhausted"

    q45 = forms.ChoiceField(label=l45, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q46 = forms.ChoiceField(label=l46, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q47 = forms.ChoiceField(label=l47, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q48 = forms.ChoiceField(label=l48, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q49 = forms.ChoiceField(label=l49, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q50 = forms.ChoiceField(label=l50, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q51 = forms.ChoiceField(label=l51, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q52 = forms.ChoiceField(label=l52, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q53 = forms.ChoiceField(label=l53, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q54 = forms.ChoiceField(label=l54, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    q55 = forms.ChoiceField(label=l55, required=True, choices=CHOICES,
                            widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))

    class Meta:
        model = Adaptability
        fields = ('q45', 'q46', 'q47', 'q48', 'q49', 'q50', 'q51', 'q52', 'q53', 'q54', 'q55')
