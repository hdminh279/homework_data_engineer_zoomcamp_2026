# Module 1 Homework: Docker & SQL & Terraform


---

## Question 1: Docker Image – pip Version

**Command**
```bash
docker run -it --entrypoint bash python:3.13
pip --version
```

**Output**
```text
pip 25.3 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)
```

**Answer:** ✅ A. 25.3

---

## Question 2: Docker Compose Networking

**Answer:**    
✅ E. db:5432  

(Containers communicate via service/container name on internal port 5432)

---

## Question 3: Trips ≤ 1 Mile (November 2025)

```sql
SELECT 
    COUNT(1) AS count
FROM green_taxi_2025_01
WHERE
    lpep_pickup_datetime >= '2025-11-01'
    AND lpep_pickup_datetime < '2025-12-01'
    AND trip_distance <= 1;
```

**Answer:** ✅ B. 8,007

---

## Question 4: Longest Trip Distance by Pickup Day

```sql
SELECT 
    DATE(lpep_pickup_datetime) AS pickup_day,
    MAX(trip_distance) AS max_distance
FROM green_taxi_2025_01
WHERE trip_distance < 100
GROUP BY DATE(lpep_pickup_datetime)
ORDER BY max_distance DESC
LIMIT 1;
```

**Answer:** ✅ A. 2025-11-14

---

## Question 5: Pickup Zone with Highest Total Amount (Nov 18, 2025)

```sql
SELECT 
    zpu."Zone" AS pickup_zone,
    SUM(gt.total_amount) AS total_amount
FROM green_taxi_2025_01 gt
JOIN zones zpu ON gt."PULocationID" = zpu."LocationID"
WHERE 
    gt.lpep_pickup_datetime >= '2025-11-18'
    AND gt.lpep_pickup_datetime < '2025-11-19'
GROUP BY zpu."Zone"
ORDER BY total_amount DESC
LIMIT 1;
```

**Answer:** ✅ A. East Harlem North

---

## Question 6: Drop-off Zone with Highest Tip  
(Pickups in East Harlem North, November 2025)

```sql
SELECT 
    zdo."Zone" AS dropoff_zone,
    gt.tip_amount
FROM green_taxi_2025_01 gt
JOIN zones zpu ON gt."PULocationID" = zpu."LocationID"
JOIN zones zdo ON gt."DOLocationID" = zdo."LocationID"
WHERE 
    gt.lpep_pickup_datetime >= '2025-11-01'
    AND gt.lpep_pickup_datetime < '2025-12-01'
    AND zpu."Zone" = 'East Harlem North'
ORDER BY gt.tip_amount DESC
LIMIT 1;
```

**Answer:** ✅ B. Yorkville West

---

## Question 7: Terraform Workflow

```text
terraform init
terraform apply -auto-approve
terraform destroy
```

**Answer:** ✅ D

---

✔ Homework completed successfully.
