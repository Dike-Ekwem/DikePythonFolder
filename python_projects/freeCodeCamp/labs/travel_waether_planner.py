distance_mi = int(17)
is_raining = bool(False)
has_bike = bool(False)
has_car = bool(True)
has_ride_share_app = bool(True)

if distance_mi == 0:
    print(False)
elif distance_mi <= 1:
    print(True) if not is_raining else print(False)
elif distance_mi > 1 and distance_mi <= 6:
    print(True) if has_bike and not is_raining else print(False)
else:
    print(True) if has_car or has_ride_share_app else print(False)