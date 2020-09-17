from django.contrib.auth.admin import admin
from gradpro.models import User, Response, SelfManagement, SocialIntelligence, Innovation, ComResponse, Communication, AdaResponse, Adaptability


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    fields = ['email', 'first_name', 'last_name']


class ResponseAdmin(admin.ModelAdmin):
    fields = ['user']

class ComResponseAdmin(admin.ModelAdmin):
    fields = ['user']

class AdaResponseAdmin(admin.ModelAdmin):
    fields = ['user']


class SelfManagementAdmin(admin.ModelAdmin):
    fields = ['response', 'score', 'concentration_score', 'adaptability_score', 'initiative_score']


class SocialIntelligenceAdmin(admin.ModelAdmin):
    fields = ['response', 'score', 'communication_score', 'collaborating_score', 'feeling_score']


class InnovationAdmin(admin.ModelAdmin):
    fields = ['response', 'score', 'sense_making_score', 'curiosity_score', 'creativity_score',
              'critical_thinking_score']


class CommunicationAdmin(admin.ModelAdmin):
    fields = ['response', 'score', 'social_composure_score', 'social_confirmation_score', 'social_experience_score',
              'appropriate_disclosure_score', 'articulation_score', 'wit_score']


class AdaptabilityAdmin(admin.ModelAdmin):
    fields = ['response', 'score', 'crisis_score', 'work_stress_score', 'creativity_score', 'uncertainty_score',
              'learning_score', 'interpersonal_score', 'cultural_score', 'physical_score']


admin.site.register(User, UserAdmin)
admin.site.register(Response, ResponseAdmin)
admin.site.register(ComResponse, ComResponseAdmin)
admin.site.register(AdaResponse, AdaResponseAdmin)
admin.site.register(SelfManagement, SelfManagementAdmin)
admin.site.register(SocialIntelligence, SocialIntelligenceAdmin)
admin.site.register(Innovation, InnovationAdmin)
admin.site.register(Communication, CommunicationAdmin)
admin.site.register(Adaptability, AdaptabilityAdmin)
