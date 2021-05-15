import datetime

from rest_framework.exceptions import ValidationError
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

ACTIVE_ZONES = [1, 2]
FAIR_CAP_DICT = [{"from_zone": 1, "to_zone": 1, "peak_fare": 30, "non_peak_fare": 25, "daily_cap": 100, "weekly_cap": 500,
                  "weekday_peak": [{"start": "07:00", "end": "10:30"}, {"start": "17:00", "end": "20:00"}],
                  "weekend_peak": [{"start": "09:00", "end": "11:00"}, {"start": "18:00", "end": "22:00"}]
                  },
                 {"from_zone": 2, "to_zone": 2, "peak_fare": 25, "non_peak_fare": 20, "daily_cap": 80, "weekly_cap": 400,
                  "weekday_peak": [{"start": "07:00", "end": "10:30"}, {"start": "17:00", "end": "20:00"}],
                  "weekend_peak": [{"start": "09:00", "end": "11:00"}, {"start": "18:00", "end": "22:00"}]
                  },
                 {"from_zone": 1, "to_zone": 2, "peak_fare": 35, "non_peak_fare": 30, "daily_cap": 120, "weekly_cap": 600,
                  "weekday_peak": [{"start": "07:00", "end": "10:30"}, {"start": "17:00", "end": "20:00"}],
                  "weekend_peak": [{"start": "09:00", "end": "11:00"}, {"start": "18:00", "end": "22:00"}]
                  },
                 {"from_zone": 2, "to_zone": 1, "peak_fare": 35, "non_peak_fare": 30, "daily_cap": 120, "weekly_cap": 600,
                  "weekday_peak": [{"start": "07:00", "end": "10:30"}],
                  "weekend_peak": [{"start": "09:00", "end": "11:00"}]
                  }]


class FairCalculatorAPI(APIView):
    renderer_classes = (JSONRenderer,)
    allowed_methods = ['POST']

    """
    Class post method to calculate fare of an individual based on the list of dates and travelling zones provided.
    Method: POST
    Request JSON: [<list of dictionary containing detail of each journey>]
                  Dictionary params : 
                  "date-time: <Datetime string in format YYYY-MM-DD HH:MM:SS>"
                  "from_zone": <int>
                  "to_zone": <int>
    Response: {"total_fare": <Calculated fare of an individual>}
    """

    # Static method to raise validation error.
    @staticmethod
    def raise_error(error_message):
        raise ValidationError(error_message)

    # Function to categorise fare based on week and days.
    def create_fare_dict(self, journey_list):
        fare_dict = dict()

        for each in journey_list:
            from_zone = each.get('from_zone')
            to_zone = each.get('to_zone')
            if from_zone and to_zone not in ACTIVE_ZONES:
                self.raise_error("Zone does not exist.")

            in_peak = False
            journey_date_time = each.get('date-time')
            date_time_obj = datetime.datetime.strptime(journey_date_time, "%Y-%m-%d %H:%M:%S")
            if date_time_obj > datetime.datetime.now():
                self.raise_error("Datetime is greater than current time.")

            day_of_week = date_time_obj.weekday()
            time_of_day = date_time_obj.time()
            date_of_fare = date_time_obj.timetuple().tm_yday
            week_number = date_time_obj.isocalendar()[1]
            travel_detail = next((travel_detail for travel_detail in FAIR_CAP_DICT
                                  if travel_detail["from_zone"] == from_zone and travel_detail["to_zone"] == to_zone), {})
            if not travel_detail:
                self.raise_error("Can not travel between these 2 zones.")

            if day_of_week < 5:
                peak_hours = travel_detail.get('weekday_peak')
            else:
                peak_hours = travel_detail.get("weekend_peak")
            for time_range in peak_hours:
                start_at = datetime.datetime.strptime(time_range.get('start'), "%H:%M")
                end_at = datetime.datetime.strptime(time_range.get('end'), "%H:%M")
                if start_at.time() <= time_of_day < end_at.time():
                    in_peak = True
                    break

            fare = travel_detail.get('peak_fare') if in_peak else travel_detail.get('non_peak_fare')
            zone_covered = 1
            if from_zone != to_zone:
                zone_covered = from_zone if from_zone > to_zone else to_zone

            if fare_dict.get(week_number):
                if fare_dict[week_number].get('day_dict'):
                    if fare_dict[week_number]['day_dict'].get(date_of_fare):
                        fare_dict[week_number]['day_dict'][date_of_fare]['fare'] += fare
                        if fare_dict[week_number]['day_dict'][date_of_fare]['zone_covered'] < zone_covered:
                            fare_dict[week_number]['day_dict'][date_of_fare]['zone_covered'] = zone_covered
                            fare_dict[week_number]['day_dict'][date_of_fare]['day_cap'] = travel_detail.get('daily_cap')
                    else:
                        fare_dict[week_number]['day_dict'][date_of_fare] = {'fare': fare, 'zone_covered': zone_covered,
                                                                            'day_cap': travel_detail.get('daily_cap')}
                fare_dict[week_number]['fare'] += fare
                if fare_dict[week_number]['zone_covered'] < zone_covered:
                    fare_dict[week_number]['zone_covered'] = zone_covered
                    fare_dict[week_number]['week_cap'] = travel_detail.get('weekly_cap')
            else:
                fare_dict[week_number] = {'day_dict': {date_of_fare: {'fare': fare, 'zone_covered': zone_covered,
                                                                      'day_cap': travel_detail.get('daily_cap')}},
                                          'fare': fare, 'zone_covered': zone_covered, 'week_cap': travel_detail.get('weekly_cap')}
        return fare_dict

    # Post method to get total fare of journey.
    def post(self, request):

        journey_list = request.data
        fare_dict = self.create_fare_dict(journey_list)

        total_fare = 0
        for week, week_detail in fare_dict.items():
            week_total = 0
            for day_detail in week_detail.get('day_dict').values():
                if day_detail['fare'] > day_detail['day_cap']:
                    week_total += day_detail['day_cap']
                else:
                    week_total += day_detail['fare']
            if week_total > week_detail['week_cap']:
                total_fare += week_detail['week_cap']
            else:
                total_fare += week_total

        response_data = {"total_fare": total_fare}
        return Response(data=response_data, content_type='application/json')
