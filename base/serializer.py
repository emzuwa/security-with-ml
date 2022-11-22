from rest_framework import serializers 
from base.models import Tutorial


 
class TutorialSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Tutorial
        # fields = ('id',
        #           'title',
        #           'description',
        #           'published')
        fields = (
                  'filename',
                  'prediction',
                  'date')