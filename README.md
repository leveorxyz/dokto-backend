# Dokto-Backend

The backend api server for the Dokto project.

## Project Directory Structure

```bash
Dokto-Backend
├── accounting
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── constant
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── core
│   ├── admin.py
│   ├── apps.py
│   ├── classes.py
│   ├── exceptions.py
│   ├── __init__.py
│   ├── literals.py
│   ├── management
│   │   └── commands
│   │       └── makesuper.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── pagination.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tests.py
│   ├── utils.py
│   └── views.py
├── dashboard
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── Dokto_Backend
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   └── wsgi.py
├── example.env
├── json
│   ├── accepted_insurance.json
│   ├── available_care.json
│   ├── city.json
│   ├── country.json
│   ├── country_phone_code.json
│   └── state.json
├── manage.py
├── Procfile
├── README.md
├── requirements.txt
├── scripts
│   ├── deploy.sh
│   └── fresh_init.sh
├── templates
│   └── email
│       ├── patient_verification.html
│       └── provider_verification.html
├── twilio_chat
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
└── user
    ├── admin.py
    ├── apps.py
    ├── __init__.py
    ├── migrations
    │   ├── 0001_initial.py
    │   ├── 0002_auto_20211014_1528.py
    │   ├── 0003_auto_20211014_1536.py
    │   ├── 0004_userip.py
    │   ├── 0005_userlanguage.py
    │   ├── 0006_alter_user_email.py
    │   ├── 0007_doctorinfo.py
    │   ├── 0008_doctorinfo_gender.py
    │   ├── 0009_alter_user_username.py
    │   ├── 0010_auto_20211017_1626.py
    │   ├── 0011_alter_user_email.py
    │   ├── 0012_auto_20211017_1829.py
    │   ├── 0013_alter_user_user_type.py
    │   ├── 0014_alter_doctorinfo_gender_squashed_0015_auto_20211018_1424.py
    │   ├── 0015_doctoreducation.py
    │   ├── 0016_auto_20211018_1820.py
    │   ├── 0017_doctorexperience_doctorspecialty.py
    │   ├── 0018_auto_20211018_1837.py
    │   ├── 0019_collectiveinfo.py
    │   ├── 0020_alter_user_user_type.py
    │   ├── 0021_pharmacyinfo.py
    │   ├── 0022_doctorexperience_doctor_info.py
    │   ├── 0023_auto_20211023_1317.py
    │   ├── 0024_patientinfo_squashed_0025_auto_20211023_1407.py
    │   ├── 0025_alter_patientinfo_insurance_type.py
    │   ├── 0026_doctoravailablehours_doctorreview.py
    │   ├── 0027_auto_20211027_1708.py
    │   ├── 0028_auto_20211030_1918.py
    │   ├── 0029_auto_20211030_1948.py
    │   ├── 0030_remove_patientinfo_username.py
    │   ├── 0031_alter_doctorinfo_gender.py
    │   ├── 0032_doctorinfo_identification_number.py
    │   ├── 0033_alter_patientinfo_gender.py
    │   ├── 0034_doctorinfo_awards.py
    │   ├── 0035_doctorinfo_license_file.py
    │   ├── 0036_patientinfo_identification_photo.py
    │   ├── 0037_alter_doctorinfo_identification_photo.py
    │   ├── 0038_auto_20211106_1440.py
    │   ├── 0039_doctorinfo_accepted_insurance.py
    │   ├── 0040_auto_20211108_1054.py
    │   └── __init__.py
    ├── models.py
    ├── serializers.py
    ├── tests.py
    ├── urls.py
    ├── utils.py
    └── views.py

19 directories, 122 files
```

## Requirements

See the requirements for this project [click here](https://github.com/ToybethSystems/Dokto-Backend/blob/main/requirements.txt).

## Installation

- First clone the prohject into your local machine.

```bash
git clone https://github.com/ToybethSystems/Dokto-Backend.git
```

- Go to the repository and create a virtual environment.

```bash
cd Dokto-Backend
python3 -m venv venv
```

- Activate the virtual environment and install dependencies.

```bash
source venv/bin/activate
pip install -r requirements.txt
```

- Copy the `example.env` file to `.env` and fill in the values.

```bash
cp example.env .env
```

- The `.env` file should look like this:

```text
SECRET_KEY=<yoursecretkey>
VERSION=v1
DEBUG=True
```

- Create and migrate the database.

```bash
python manage.py migrate
```

## Running the server

- You can run the server with the following command:

```bash
python manage.py runserver
```

- You can also run the server on a custom port by adding the port number after the `runserver` command:

```bash
python manage.py runserver 8000
```
