from rest_framework import serializers
from datetime import datetime


class InputSerializer(serializers.Serializer):
    """
    Will be used to validate the dat range entered in th e search
    """
    start_date = serializers.CharField(max_length=10, allow_blank=False, trim_whitespace=True)
    end_date = serializers.CharField(max_length=10, allow_blank=False, trim_whitespace=True)

    def validate(self, data):
        try:
            start = datetime.strptime(data['start_date'], "%Y-%m-%d")
            end = datetime.strptime(data['end_date'], "%Y-%m-%d")
            diff = (end - start).days
            if diff > 7 or diff < 1:
                raise ValueError("Date Range must be greater than 1 but less than 7")
            return data
        except (Exception, ValueError, TypeError) as e:
            raise serializers.ValidationError(str(e))
