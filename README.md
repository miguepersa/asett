## Django API for Doctor, Patient, and Appointment Management

This API provides endpoints for managing doctor, patient, and appointment data.

## Authentication

The API uses Django's authentication framework to restrict access to certain endpoints. Users must be logged in to access endpoints related to their own patient or doctor profile.

## Endpoints

### DoctorViewSet

* GET /doctors/: Retrieves a list of all doctors.
* POST /doctors/: Creates a new doctor profile.

### PatientViewSet

* GET /patients/: Retrieves a list of all patients.
* POST /patients/: Creates a new patient profile.

### AppointmentViewSet

* GET /appointments/: Retrieves a list of appointments. For doctors, it returns appointments for their patients. For patients, it returns appointments for themselves.
* POST /appointments/: Creates a new appointment.

## Error Handling

The API will return appropriate HTTP status codes and error messages in case of any errors. For example, if a user attempts to create a new appointment with a doctor who is not available during the requested time slot, the API will return a 400 Bad Request error with a message indicating the conflict.

## Usage

### Doctor

To create a new doctor profile, make a POST request to `/doctors/` with the following JSON data:

```
json
{
  "user": <user_id>,
  "name": "<doctor_name>"
}
```

Replace `<user_id>` with the ID of the user who will be associated with the doctor profile. Replace `<doctor_name>` with the doctor's name.

### Patient

To create a new patient profile, make a POST request to `/patients/` with the following JSON data:

```
json
{
  "user": <user_id>,
  "name": "<patient_name>",
  "can_login": <boolean>
}
```


Replace `<user_id>` with the ID of the user who will be associated with the patient profile. Replace `<patient_name>` with the patient's name. Replace `<boolean>` with `true` if the patient should be able to log in to the system, or `false` if they should not.

### Appointment

To create a new appointment, make a POST request to `/appointments/` with the following JSON data:

```
json
{
  "doctor": <doctor_id>,
  "start_time": "<start_time>",
  "end_time": "<end_time>"
}
```


Replace `<doctor_id>` with the ID of the doctor the patient wants to schedule an appointment with. Replace `<start_time>` and `<end_time>` with the desired appointment time slot in ISO 8601 format (e.g., `2023-10-04T10:00:00Z`).

## Error Handling

The API will return appropriate HTTP status codes and error messages in case of any errors. For example, if a user attempts to create a new appointment with a doctor who is not available during the requested time slot, the API will return a 400 Bad Request error with a message indicating the conflict.

