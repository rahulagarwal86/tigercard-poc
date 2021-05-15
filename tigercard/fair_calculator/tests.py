import datetime
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class ConfidenceAPITests(APITestCase):

    def base_api_test_function(self, request_data, response_fare):
        url = reverse('calculate-fare')
        response = self.client.post(url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'total_fare': response_fare})

    def test_zone_1_peak_travel(self):
        data = [{"date-time": "2021-05-03 10:20:00", "from_zone": 1, "to_zone": 1}
                ]
        self.base_api_test_function(request_data=data, response_fare=30)

    def test_zone_2_peak_travel(self):
        data = [{"date-time": "2021-05-03 10:20:00", "from_zone": 2, "to_zone": 2}
                ]
        self.base_api_test_function(request_data=data, response_fare=25)

    def test_zone_1_2_peak_travel(self):
        data = [{"date-time": "2021-05-03 10:20:00", "from_zone": 1, "to_zone": 2}
                ]
        self.base_api_test_function(request_data=data, response_fare=35)

    def test_zone_2_1_eve_peak_travel(self):
        data = [{"date-time": "2021-05-03 17:20:00", "from_zone": 2, "to_zone": 1}
                ]
        self.base_api_test_function(request_data=data, response_fare=30)

    def test_zone_1_off_peak_travel(self):
        data = [{"date-time": "2021-05-03 12:20:00", "from_zone": 1, "to_zone": 1}
                ]
        self.base_api_test_function(request_data=data, response_fare=25)

    def test_zone_2_off_peak_travel(self):
        data = [{"date-time": "2021-05-03 12:20:00", "from_zone": 2, "to_zone": 2}
                ]
        self.base_api_test_function(request_data=data, response_fare=20)

    def test_zone_1_2_off_peak_travel(self):
        data = [{"date-time": "2021-05-03 12:20:00", "from_zone": 1, "to_zone": 2}
                ]
        self.base_api_test_function(request_data=data, response_fare=30)

    def test_zone_2_1_off_peak_travel(self):
        data = [{"date-time": "2021-05-03 12:20:00", "from_zone": 2, "to_zone": 1}
                ]
        self.base_api_test_function(request_data=data, response_fare=30)

    def test_zone_at_start_of_peak_travel(self):
        data = [{"date-time": "2021-05-03 07:00:00", "from_zone": 1, "to_zone": 1}
                ]
        self.base_api_test_function(request_data=data, response_fare=30)

    def test_zone_at_end_of_peak_travel(self):
        data = [{"date-time": "2021-05-03 10:30:00", "from_zone": 1, "to_zone": 1}
                ]
        self.base_api_test_function(request_data=data, response_fare=25)

    def test_no_cap_travel(self):
        data = [{"date-time": "2021-05-03 8:00:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-03 8:30:00", "from_zone": 1, "to_zone": 1}
                ]
        self.base_api_test_function(request_data=data, response_fare=60)

    def test_cap_travel_zone_1(self):
        data = [{"date-time": "2021-05-03 8:00:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-03 9:00:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-03 13:00:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-03 14:00:00", "from_zone": 1, "to_zone": 1}
                ]
        self.base_api_test_function(request_data=data, response_fare=100)

    def test_cap_travel_weekend_zone_2(self):
        data = [{"date-time": "2021-05-01 9:00:00", "from_zone": 2, "to_zone": 2},
                {"date-time": "2021-05-01 10:00:00", "from_zone": 2, "to_zone": 2},
                {"date-time": "2021-05-01 16:00:00", "from_zone": 2, "to_zone": 2},
                {"date-time": "2021-05-01 17:00:00", "from_zone": 2, "to_zone": 2}
                ]
        self.base_api_test_function(request_data=data, response_fare=80)

    def test_cap_not_applicable_between_zone_travel(self):
        data = [{"date-time": "2021-05-04 8:00:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-04 9:00:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-04 13:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2021-05-04 14:00:00", "from_zone": 2, "to_zone": 2}
                ]
        self.base_api_test_function(request_data=data, response_fare=110)

    def test_cap_applicable_between_zone_travel(self):
        data = [{"date-time": "2021-05-04 8:00:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-04 9:00:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-04 13:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2021-05-04 14:00:00", "from_zone": 2, "to_zone": 2},
                {"date-time": "2021-05-04 17:00:00", "from_zone": 2, "to_zone": 1}
                ]
        self.base_api_test_function(request_data=data, response_fare=120)

    def test_no_cap_reached(self):
        data = [{"date-time": "2021-05-03 8:00:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-04 9:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2021-05-05 13:00:00", "from_zone": 2, "to_zone": 2},
                ]
        self.base_api_test_function(request_data=data, response_fare=85)

    def test_day_response(self):
        data = [{"date-time": "2021-05-03 10:20:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2021-05-03 10:45:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-03 16:15:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-03 18:15:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-03 19:00:00", "from_zone": 1, "to_zone": 2}
                ]

        self.base_api_test_function(request_data=data, response_fare=120)

    def test_weekly_cap_not_applicable(self):
        data = [{"date-time": "2021-05-03 10:20:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2021-05-04 10:45:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-05 16:15:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-10 18:15:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-11 19:00:00", "from_zone": 1, "to_zone": 2}
                ]

        self.base_api_test_function(request_data=data, response_fare=150)


    def test_week_response(self):
        data = [{"date-time": "2021-05-03 10:20:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2021-05-03 10:45:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-03 16:15:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-03 18:15:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-03 19:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2021-05-04 10:20:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2021-05-04 10:45:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-04 16:15:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-04 18:15:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-04 19:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2021-05-05 10:20:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2021-05-05 10:45:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-05 16:15:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-05 18:15:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-05 19:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2021-05-06 10:20:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2021-05-06 10:45:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-06 16:15:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-06 18:15:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-06 19:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2021-05-07 16:15:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-07 15:15:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-07 19:00:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-08 10:20:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2021-05-08 10:45:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-08 16:15:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-08 18:15:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-08 19:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2021-05-09 10:20:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2021-05-09 10:45:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-09 16:15:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-09 18:15:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-09 19:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2021-05-10 07:20:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2021-05-10 10:00:00", "from_zone": 2, "to_zone": 2},
                {"date-time": "2021-05-10 12:15:00", "from_zone": 2, "to_zone": 2},
                {"date-time": "2021-05-10 13:15:00", "from_zone": 2, "to_zone": 2}
                ]
        self.base_api_test_function(request_data=data, response_fare=700)

    def test_week_cap(self):
        data = [{"date-time": "2021-03-01 07:00:00", "from_zone": 2, "to_zone": 2},
                {"date-time": "2021-03-01 12:00:00", "from_zone": 2, "to_zone": 2},
                {"date-time": "2021-03-01 18:00:00", "from_zone": 2, "to_zone": 2},
                {"date-time": "2021-03-02 07:00:00", "from_zone": 2, "to_zone": 2},
                {"date-time": "2021-03-02 12:00:00", "from_zone": 2, "to_zone": 2},
                {"date-time": "2021-03-02 18:00:00", "from_zone": 2, "to_zone": 2},
                {"date-time": "2021-03-03 07:00:00", "from_zone": 2, "to_zone": 2},
                {"date-time": "2021-03-03 12:00:00", "from_zone": 2, "to_zone": 2},
                {"date-time": "2021-03-03 18:00:00", "from_zone": 2, "to_zone": 2},
                {"date-time": "2021-03-04 07:00:00", "from_zone": 2, "to_zone": 2},
                {"date-time": "2021-03-04 12:00:00", "from_zone": 2, "to_zone": 2},
                {"date-time": "2021-03-04 18:00:00", "from_zone": 2, "to_zone": 2},
                {"date-time": "2021-03-05 07:00:00", "from_zone": 2, "to_zone": 2},
                {"date-time": "2021-03-05 12:00:00", "from_zone": 2, "to_zone": 2},
                {"date-time": "2021-03-05 18:00:00", "from_zone": 2, "to_zone": 2},
                {"date-time": "2021-03-06 09:00:00", "from_zone": 2, "to_zone": 2},
                {"date-time": "2021-03-06 12:00:00", "from_zone": 2, "to_zone": 2},
                {"date-time": "2021-03-06 18:00:00", "from_zone": 2, "to_zone": 2},
                {"date-time": "2021-03-07 09:00:00", "from_zone": 2, "to_zone": 2},
                {"date-time": "2021-03-07 12:00:00", "from_zone": 2, "to_zone": 2},
                {"date-time": "2021-03-07 18:00:00", "from_zone": 2, "to_zone": 2}]
        self.base_api_test_function(request_data=data, response_fare=400)

    def test_daily_cap(self):
        data = [{"date-time": "2021-03-01 07:00:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-03-01 12:00:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-03-01 18:00:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-03-01 04:59:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-03-03 07:00:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-03-03 12:00:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-03-03 18:00:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-03-03 04:59:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-03-05 07:00:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-03-05 12:00:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-03-05 18:00:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-03-05 04:59:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-03-07 09:00:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-03-07 12:00:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-03-07 18:00:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-03-07 05:59:00", "from_zone": 1, "to_zone": 1}
                ]
        self.base_api_test_function(request_data=data, response_fare=400)

    def test_enter_zone_1_in_peak_hour(self):
        data = [{"date-time": "2021-03-01 17:00:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2021-03-01 18:00:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-03-01 19:00:00", "from_zone": 1, "to_zone": 2}
                ]
        self.base_api_test_function(request_data=data, response_fare=95)

    def test_enter_zone_2_in_peak_hour(self):
        data = [{"date-time": "2021-03-01 17:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2021-03-01 18:00:00", "from_zone": 2, "to_zone": 2},
                {"date-time": "2021-03-01 19:00:00", "from_zone": 2, "to_zone": 1}
                ]
        self.base_api_test_function(request_data=data, response_fare=90)

    def test_week_and_day_cap(self):
        data = [{"date-time": "2021-05-03 10:20:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2021-05-03 10:45:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-03 16:15:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-03 18:15:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-03 19:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2021-05-04 10:20:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2021-05-04 10:45:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-04 16:15:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-04 18:15:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-04 19:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2021-05-05 10:20:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2021-05-05 10:45:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-05 16:15:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-05 18:15:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-05 19:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2021-05-06 10:20:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2021-05-06 10:45:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-06 16:15:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-06 18:15:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-06 19:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2021-05-07 16:15:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-07 15:15:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-07 19:00:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-08 10:20:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2021-05-08 10:45:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-08 16:15:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-08 18:15:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-08 19:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2021-05-09 10:20:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2021-05-09 10:45:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-09 16:15:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-09 18:15:00", "from_zone": 1, "to_zone": 1},
                {"date-time": "2021-05-09 19:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2021-05-10 07:20:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2021-05-10 10:00:00", "from_zone": 2, "to_zone": 2},
                {"date-time": "2021-05-10 12:15:00", "from_zone": 2, "to_zone": 2},
                {"date-time": "2021-05-10 13:15:00", "from_zone": 2, "to_zone": 2},
                {"date-time": "2021-05-10 15:15:00", "from_zone": 2, "to_zone": 2},
                {"date-time": "2021-05-10 18:15:00", "from_zone": 2, "to_zone": 1},
                ]
        self.base_api_test_function(request_data=data, response_fare=720)

    def test_monthly_fare(self):
        data = [{"date-time": "2020-01-01 09:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2020-01-02 09:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2020-01-03 09:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2020-01-04 09:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2020-01-05 09:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2020-01-06 09:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2020-01-07 09:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2020-01-08 09:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2020-01-09 09:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2020-01-10 09:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2020-01-11 09:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2020-01-12 09:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2020-01-13 09:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2020-01-14 09:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2020-01-15 09:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2020-01-16 09:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2020-01-17 09:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2020-01-18 09:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2020-01-19 09:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2020-01-20 09:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2020-01-21 09:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2020-01-22 09:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2020-01-23 09:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2020-01-24 09:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2020-01-25 09:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2020-01-26 09:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2020-01-27 09:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2020-01-28 09:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2020-01-29 09:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2020-01-30 09:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2020-01-31 09:00:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2020-01-01 20:00:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2020-01-02 20:00:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2020-01-03 20:00:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2020-01-04 20:00:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2020-01-05 20:00:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2020-01-06 20:00:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2020-01-07 20:00:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2020-01-08 20:00:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2020-01-09 20:00:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2020-01-10 20:00:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2020-01-11 20:00:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2020-01-12 20:00:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2020-01-13 20:00:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2020-01-14 20:00:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2020-01-15 20:00:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2020-01-16 20:00:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2020-01-17 20:00:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2020-01-18 20:00:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2020-01-19 20:00:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2020-01-20 20:00:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2020-01-21 20:00:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2020-01-22 20:00:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2020-01-23 20:00:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2020-01-24 20:00:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2020-01-25 20:00:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2020-01-26 20:00:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2020-01-27 20:00:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2020-01-28 20:00:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2020-01-29 20:00:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2020-01-30 20:00:00", "from_zone": 2, "to_zone": 1},
                {"date-time": "2020-01-31 20:00:00", "from_zone": 2, "to_zone": 1}
                ]
        self.base_api_test_function(request_data=data, response_fare=2015)

    def test_future_date_error(self):
        url = reverse('calculate-fare')

        future_date = datetime.datetime.now() + datetime.timedelta(days=2)
        future_date = future_date.strftime("%Y-%m-%d %H:%M:%S")
        data = [{"date-time": "2021-05-03 10:20:00", "from_zone": 2, "to_zone": 1},
                {"date-time": future_date, "from_zone": 1, "to_zone": 1}
                ]

        response = self.client.post(url, data, format='json')
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.exception, True)

    def test_no_zone_error(self):
        url = reverse('calculate-fare')
        data = [{"date-time": "2021-05-03 10:20:00", "from_zone": 1, "to_zone": 2},
                {"date-time": "2021-05-03 10:20:00", "from_zone": 2, "to_zone": 3}
                ]
        response = self.client.post(url, data, format='json')
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.exception, True)

    def test_get_not_allowed(self):
        url = reverse('calculate-fare')
        data = []

        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
