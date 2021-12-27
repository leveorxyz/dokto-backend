--
-- PostgreSQL database dump
--

-- Dumped from database version 13.4
-- Dumped by pg_dump version 13.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: appointment_appointment; Type: TABLE; Schema: public; Owner: sihan
--

CREATE TABLE public.appointment_appointment (
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    description text NOT NULL,
    date date NOT NULL,
    start_time time without time zone NOT NULL,
    end_time time without time zone NOT NULL,
    number_of_patients integer NOT NULL,
    payment_status boolean NOT NULL,
    transaction_id character varying(100),
    patient_status character varying(50),
    doctor_id uuid NOT NULL,
    patient_id uuid NOT NULL
);


ALTER TABLE public.appointment_appointment OWNER TO sihan;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: sihan
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO sihan;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: sihan
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO sihan;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sihan
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: sihan
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO sihan;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: sihan
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO sihan;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sihan
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: sihan
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO sihan;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: sihan
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO sihan;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sihan
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: authtoken_token; Type: TABLE; Schema: public; Owner: sihan
--

CREATE TABLE public.authtoken_token (
    key character varying(40) NOT NULL,
    created timestamp with time zone NOT NULL,
    user_id uuid NOT NULL
);


ALTER TABLE public.authtoken_token OWNER TO sihan;

--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: sihan
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id uuid NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO sihan;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: sihan
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO sihan;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sihan
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: sihan
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO sihan;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: sihan
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO sihan;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sihan
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: sihan
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO sihan;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: sihan
--

CREATE SEQUENCE public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO sihan;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sihan
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: sihan
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO sihan;

--
-- Name: django_site; Type: TABLE; Schema: public; Owner: sihan
--

CREATE TABLE public.django_site (
    id integer NOT NULL,
    domain character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.django_site OWNER TO sihan;

--
-- Name: django_site_id_seq; Type: SEQUENCE; Schema: public; Owner: sihan
--

CREATE SEQUENCE public.django_site_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_site_id_seq OWNER TO sihan;

--
-- Name: django_site_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sihan
--

ALTER SEQUENCE public.django_site_id_seq OWNED BY public.django_site.id;


--
-- Name: ehr_assessmentdiagnosis; Type: TABLE; Schema: public; Owner: sihan
--

CREATE TABLE public.ehr_assessmentdiagnosis (
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    icd character varying(100),
    icd_description character varying(512),
    disease_code character varying(100),
    disease_description character varying(512),
    disease_name character varying(256),
    start_date date,
    end_date date,
    diagnosis_type character varying(25),
    primary_diagnosis boolean,
    assessment character varying(512),
    patient_encounter_id uuid NOT NULL
);


ALTER TABLE public.ehr_assessmentdiagnosis OWNER TO sihan;

--
-- Name: ehr_chiefcomplaintsandhpi; Type: TABLE; Schema: public; Owner: sihan
--

CREATE TABLE public.ehr_chiefcomplaintsandhpi (
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    "chiefComplaint" character varying(125),
    location character varying(100),
    severity character varying(125),
    duration character varying(125),
    modifying_factors character varying(125),
    associated_symptons character varying(100),
    description character varying(512),
    context character varying(100),
    hpi character varying(512),
    patient_encounter_id uuid NOT NULL,
    timing character varying(512)
);


ALTER TABLE public.ehr_chiefcomplaintsandhpi OWNER TO sihan;

--
-- Name: ehr_functionalandcognitivestatus; Type: TABLE; Schema: public; Owner: sihan
--

CREATE TABLE public.ehr_functionalandcognitivestatus (
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    "moduleType" character varying(125),
    "codeType" character varying(125),
    status character varying(125),
    code character varying(100),
    start_date date,
    description character varying(512),
    patient_encounter_id uuid NOT NULL
);


ALTER TABLE public.ehr_functionalandcognitivestatus OWNER TO sihan;

--
-- Name: ehr_icds; Type: TABLE; Schema: public; Owner: sihan
--

CREATE TABLE public.ehr_icds (
    id bigint NOT NULL,
    code_description character varying(200),
    icd_code character varying(20),
    full_description character varying(1024)
);


ALTER TABLE public.ehr_icds OWNER TO sihan;

--
-- Name: ehr_icds_id_seq; Type: SEQUENCE; Schema: public; Owner: sihan
--

CREATE SEQUENCE public.ehr_icds_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ehr_icds_id_seq OWNER TO sihan;

--
-- Name: ehr_icds_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sihan
--

ALTER SEQUENCE public.ehr_icds_id_seq OWNED BY public.ehr_icds.id;


--
-- Name: ehr_orders; Type: TABLE; Schema: public; Owner: sihan
--

CREATE TABLE public.ehr_orders (
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    lab_order text,
    imaging_order text,
    patient_encounter_id uuid NOT NULL
);


ALTER TABLE public.ehr_orders OWNER TO sihan;

--
-- Name: ehr_patientencounters; Type: TABLE; Schema: public; Owner: sihan
--

CREATE TABLE public.ehr_patientencounters (
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    visit_date date,
    location character varying(250),
    reason character varying(512),
    signed boolean,
    patient_id uuid NOT NULL,
    provider_id uuid NOT NULL,
    timing character varying(512)
);


ALTER TABLE public.ehr_patientencounters OWNER TO sihan;

--
-- Name: ehr_patientprocedure; Type: TABLE; Schema: public; Owner: sihan
--

CREATE TABLE public.ehr_patientprocedure (
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    procedure_type character varying(125),
    code character varying(100),
    description character varying(512),
    status character varying(125),
    date date,
    patient_encounter_id uuid NOT NULL
);


ALTER TABLE public.ehr_patientprocedure OWNER TO sihan;

--
-- Name: ehr_patientsocialhistory; Type: TABLE; Schema: public; Owner: sihan
--

CREATE TABLE public.ehr_patientsocialhistory (
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    home_environment character varying(100),
    children integer,
    highest_education character varying(100),
    occupation character varying(100),
    sexual_orientation character varying(100),
    gender_identity character varying(100),
    tobacco_status character varying(100),
    tobacco_type character varying(100),
    tobacco_started_year date,
    tobacco_packs_per_day character varying(100),
    tobacco_start_date date,
    tobacco_end_date date,
    tobacco_cessation character varying(100),
    exercise character varying(100),
    drug_use character varying(100),
    quit_date date,
    seatbelts character varying(100),
    exposure character varying(100),
    alcohol_use character varying(100),
    caffeine_use character varying(100),
    etoh character varying(100),
    patient_encounter_id uuid NOT NULL,
    marital_status character varying(100)
);


ALTER TABLE public.ehr_patientsocialhistory OWNER TO sihan;

--
-- Name: ehr_physicalexam; Type: TABLE; Schema: public; Owner: sihan
--

CREATE TABLE public.ehr_physicalexam (
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    general_appearance character varying(512),
    head character varying(512),
    eyes character varying(512),
    ears character varying(512),
    nose character varying(512),
    throat character varying(512),
    neck character varying(512),
    cardiac character varying(512),
    lungs character varying(512),
    abdomen character varying(512),
    musculoskeletal character varying(512),
    back character varying(512),
    extremities character varying(512),
    lower_extremities character varying(512),
    neurological character varying(512),
    skin character varying(512),
    res character varying(512),
    psychiatric character varying(512),
    rectal character varying(512),
    patient_encounter_id uuid NOT NULL
);


ALTER TABLE public.ehr_physicalexam OWNER TO sihan;

--
-- Name: ehr_planofcare; Type: TABLE; Schema: public; Owner: sihan
--

CREATE TABLE public.ehr_planofcare (
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    medical_notes text NOT NULL,
    notes_html text,
    patient_encounter_id uuid NOT NULL
);


ALTER TABLE public.ehr_planofcare OWNER TO sihan;

--
-- Name: ehr_reviewofsystem; Type: TABLE; Schema: public; Owner: sihan
--

CREATE TABLE public.ehr_reviewofsystem (
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    general character varying(512),
    head character varying(512),
    eyes character varying(512),
    ears character varying(512),
    nose character varying(512),
    mouth character varying(512),
    neck character varying(512),
    breast character varying(512),
    chest character varying(512),
    heart character varying(512),
    abdomen character varying(512),
    gu character varying(512),
    gyn character varying(512),
    musculoskeletal character varying(512),
    neurologic character varying(512),
    psychiatric character varying(512),
    patient_encounter_id uuid NOT NULL
);


ALTER TABLE public.ehr_reviewofsystem OWNER TO sihan;

--
-- Name: ehr_vitals; Type: TABLE; Schema: public; Owner: sihan
--

CREATE TABLE public.ehr_vitals (
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    reading_date date,
    reading_time time without time zone,
    height double precision,
    weight double precision,
    bmi double precision,
    temperature double precision,
    pulse double precision,
    respiratory_rate double precision,
    o2_saturation double precision,
    pain double precision,
    blood_pressure double precision,
    patient_encounter_id uuid NOT NULL
);


ALTER TABLE public.ehr_vitals OWNER TO sihan;

--
-- Name: inbox_inboxchannel; Type: TABLE; Schema: public; Owner: sihan
--

CREATE TABLE public.inbox_inboxchannel (
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    first_user_id uuid NOT NULL,
    second_user_id uuid NOT NULL
);


ALTER TABLE public.inbox_inboxchannel OWNER TO sihan;

--
-- Name: inbox_inboxmessage; Type: TABLE; Schema: public; Owner: sihan
--

CREATE TABLE public.inbox_inboxmessage (
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    message text,
    subject character varying(128),
    read_status boolean NOT NULL,
    channel_id uuid NOT NULL,
    sender_id uuid NOT NULL
);


ALTER TABLE public.inbox_inboxmessage OWNER TO sihan;

--
-- Name: twilio_chat_waitingroom; Type: TABLE; Schema: public; Owner: sihan
--

CREATE TABLE public.twilio_chat_waitingroom (
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    text character varying(200),
    room_media character varying(100),
    doctor_id uuid NOT NULL,
    room_media_mime_type character varying(100)
);


ALTER TABLE public.twilio_chat_waitingroom OWNER TO sihan;

--
-- Name: user_clinicinfo; Type: TABLE; Schema: public; Owner: sihan
--

CREATE TABLE public.user_clinicinfo (
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    username character varying(150) NOT NULL,
    number_of_practitioners integer,
    user_id uuid NOT NULL,
    notification_email character varying(254),
    website character varying(200),
    _license_file character varying(100),
    license_expiration date
);


ALTER TABLE public.user_clinicinfo OWNER TO sihan;

--
-- Name: user_doctoracceptedinsurance; Type: TABLE; Schema: public; Owner: sihan
--

CREATE TABLE public.user_doctoracceptedinsurance (
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    insurance character varying(50) NOT NULL,
    doctor_info_id uuid NOT NULL
);


ALTER TABLE public.user_doctoracceptedinsurance OWNER TO sihan;

--
-- Name: user_doctoravailablehours; Type: TABLE; Schema: public; Owner: sihan
--

CREATE TABLE public.user_doctoravailablehours (
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    day_of_week character varying(3),
    start_time time without time zone,
    end_time time without time zone,
    doctor_info_id uuid NOT NULL
);


ALTER TABLE public.user_doctoravailablehours OWNER TO sihan;

--
-- Name: user_doctoreducation; Type: TABLE; Schema: public; Owner: sihan
--

CREATE TABLE public.user_doctoreducation (
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    course character varying(50) NOT NULL,
    year character varying(15) NOT NULL,
    college character varying(60) NOT NULL,
    doctor_info_id uuid NOT NULL
);


ALTER TABLE public.user_doctoreducation OWNER TO sihan;

--
-- Name: user_doctorexperience; Type: TABLE; Schema: public; Owner: sihan
--

CREATE TABLE public.user_doctorexperience (
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    establishment_name character varying(50) NOT NULL,
    job_title character varying(50) NOT NULL,
    start_date date NOT NULL,
    end_date date,
    job_description text,
    doctor_info_id uuid NOT NULL
);


ALTER TABLE public.user_doctorexperience OWNER TO sihan;

--
-- Name: user_doctorinfo; Type: TABLE; Schema: public; Owner: sihan
--

CREATE TABLE public.user_doctorinfo (
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    username character varying(150) NOT NULL,
    date_of_birth date,
    country character varying(50),
    gender character varying(30),
    identification_type character varying(20),
    identification_number character varying(50),
    _identification_photo character varying(100),
    professional_bio text,
    linkedin_url character varying(200),
    facebook_url character varying(200),
    twitter_url character varying(200),
    awards text,
    _license_file character varying(100),
    notification_email character varying(254),
    reason_to_delete character varying(2000),
    temporary_disable boolean NOT NULL,
    accepted_insurance character varying(100),
    user_id uuid NOT NULL,
    profession character varying(100),
    license_expiration date
);


ALTER TABLE public.user_doctorinfo OWNER TO sihan;

--
-- Name: user_doctorlanguage; Type: TABLE; Schema: public; Owner: sihan
--

CREATE TABLE public.user_doctorlanguage (
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    language character varying(20) NOT NULL,
    doctor_info_id uuid NOT NULL
);


ALTER TABLE public.user_doctorlanguage OWNER TO sihan;

--
-- Name: user_doctorreview; Type: TABLE; Schema: public; Owner: sihan
--

CREATE TABLE public.user_doctorreview (
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    patient_name character varying(80),
    star_count double precision,
    comment text,
    doctor_info_id uuid NOT NULL
);


ALTER TABLE public.user_doctorreview OWNER TO sihan;

--
-- Name: user_doctorspecialty; Type: TABLE; Schema: public; Owner: sihan
--

CREATE TABLE public.user_doctorspecialty (
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    specialty character varying(50) NOT NULL,
    doctor_info_id uuid NOT NULL
);


ALTER TABLE public.user_doctorspecialty OWNER TO sihan;

--
-- Name: user_passwordresetwhitelist; Type: TABLE; Schema: public; Owner: sihan
--

CREATE TABLE public.user_passwordresetwhitelist (
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    email character varying(254) NOT NULL,
    token character varying(255) NOT NULL
);


ALTER TABLE public.user_passwordresetwhitelist OWNER TO sihan;

--
-- Name: user_patientinfo; Type: TABLE; Schema: public; Owner: sihan
--

CREATE TABLE public.user_patientinfo (
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    gender character varying(20) NOT NULL,
    date_of_birth date NOT NULL,
    identification_type character varying(20) NOT NULL,
    identification_number character varying(50) NOT NULL,
    _identification_photo character varying(100),
    insurance_type character varying(20) NOT NULL,
    insurance_name character varying(50),
    insurance_number character varying(50),
    insurance_policy_holder_name character varying(50),
    referring_doctor_full_name character varying(50),
    referring_doctor_phone_number character varying(20),
    referring_doctor_address character varying(100),
    name_of_parent character varying(100),
    user_id uuid NOT NULL,
    display_id integer NOT NULL,
    notification_email character varying(254),
    CONSTRAINT user_patientinfo_display_id_check CHECK ((display_id >= 0))
);


ALTER TABLE public.user_patientinfo OWNER TO sihan;

--
-- Name: user_pharmacyinfo; Type: TABLE; Schema: public; Owner: sihan
--

CREATE TABLE public.user_pharmacyinfo (
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    username character varying(150) NOT NULL,
    number_of_practitioners integer,
    user_id uuid NOT NULL,
    notification_email character varying(254)
);


ALTER TABLE public.user_pharmacyinfo OWNER TO sihan;

--
-- Name: user_user; Type: TABLE; Schema: public; Owner: sihan
--

CREATE TABLE public.user_user (
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    full_name character varying(180) NOT NULL,
    email character varying(254) NOT NULL,
    user_type character varying(20) NOT NULL,
    is_verified boolean,
    street character varying(100),
    state character varying(50),
    city character varying(50),
    zip_code character varying(15),
    contact_no character varying(20),
    _profile_photo character varying(100)
);


ALTER TABLE public.user_user OWNER TO sihan;

--
-- Name: user_user_groups; Type: TABLE; Schema: public; Owner: sihan
--

CREATE TABLE public.user_user_groups (
    id bigint NOT NULL,
    user_id uuid NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.user_user_groups OWNER TO sihan;

--
-- Name: user_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: sihan
--

CREATE SEQUENCE public.user_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_user_groups_id_seq OWNER TO sihan;

--
-- Name: user_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sihan
--

ALTER SEQUENCE public.user_user_groups_id_seq OWNED BY public.user_user_groups.id;


--
-- Name: user_user_user_permissions; Type: TABLE; Schema: public; Owner: sihan
--

CREATE TABLE public.user_user_user_permissions (
    id bigint NOT NULL,
    user_id uuid NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.user_user_user_permissions OWNER TO sihan;

--
-- Name: user_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: sihan
--

CREATE SEQUENCE public.user_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_user_user_permissions_id_seq OWNER TO sihan;

--
-- Name: user_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sihan
--

ALTER SEQUENCE public.user_user_user_permissions_id_seq OWNED BY public.user_user_user_permissions.id;


--
-- Name: user_userip; Type: TABLE; Schema: public; Owner: sihan
--

CREATE TABLE public.user_userip (
    id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone,
    ip_address inet NOT NULL,
    user_id uuid NOT NULL
);


ALTER TABLE public.user_userip OWNER TO sihan;

--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Name: django_site id; Type: DEFAULT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.django_site ALTER COLUMN id SET DEFAULT nextval('public.django_site_id_seq'::regclass);


--
-- Name: ehr_icds id; Type: DEFAULT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.ehr_icds ALTER COLUMN id SET DEFAULT nextval('public.ehr_icds_id_seq'::regclass);


--
-- Name: user_user_groups id; Type: DEFAULT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_user_groups ALTER COLUMN id SET DEFAULT nextval('public.user_user_groups_id_seq'::regclass);


--
-- Name: user_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.user_user_user_permissions_id_seq'::regclass);


--
-- Data for Name: appointment_appointment; Type: TABLE DATA; Schema: public; Owner: sihan
--

COPY public.appointment_appointment (id, created_at, updated_at, is_deleted, deleted_at, description, date, start_time, end_time, number_of_patients, payment_status, transaction_id, patient_status, doctor_id, patient_id) FROM stdin;
b4208189-9eee-452a-86fc-1971c2df9648	2021-11-30 02:18:34.940333+00	2021-11-30 02:18:34.940396+00	f	\N	tooth ache	2021-11-30	10:30:00	11:00:00	1	t	string	new patient	a354ca46-0d86-4f96-8cdb-590a8986513b	b54ff328-3635-4084-a160-e1e98f65b47e
c897ef47-ab8c-44a0-aff7-326428b17c2c	2021-11-30 02:19:27.933577+00	2021-11-30 02:19:27.933623+00	f	\N	head ache	2021-11-30	10:30:00	11:00:00	2	t	string	recovering	90714f3d-d654-4c8e-b15d-2a08d819f96c	a5e1d84b-6365-4d91-a62e-12f9d226a7ca
c896b77f-43f8-4264-bf07-d46f4ca6dd64	2021-11-30 02:20:29.612018+00	2021-11-30 02:20:29.612081+00	f	\N	heart ache	2021-11-30	11:00:00	11:30:00	1	t	string	new patient	4fb7958b-94e4-4354-a641-3023a788ccc1	2b59a0f4-1707-482f-bcb8-2793a300b390
36360d19-c441-470e-a6aa-1b73e350ef6f	2021-11-30 02:20:50.312963+00	2021-11-30 02:20:50.313022+00	f	\N	heart ache	2021-11-30	11:00:00	11:30:00	1	t	string	new patient	0440043c-e650-410a-ab98-4fe6ba519ace	2b59a0f4-1707-482f-bcb8-2793a300b390
\.


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: sihan
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: sihan
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: sihan
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add content type	4	add_contenttype
14	Can change content type	4	change_contenttype
15	Can delete content type	4	delete_contenttype
16	Can view content type	4	view_contenttype
17	Can add session	5	add_session
18	Can change session	5	change_session
19	Can delete session	5	delete_session
20	Can view session	5	view_session
21	Can add site	6	add_site
22	Can change site	6	change_site
23	Can delete site	6	delete_site
24	Can view site	6	view_site
25	Can add Token	7	add_token
26	Can change Token	7	change_token
27	Can delete Token	7	delete_token
28	Can view Token	7	view_token
29	Can add token	8	add_tokenproxy
30	Can change token	8	change_tokenproxy
31	Can delete token	8	delete_tokenproxy
32	Can view token	8	view_tokenproxy
33	Can add user	9	add_user
34	Can change user	9	change_user
35	Can delete user	9	delete_user
36	Can view user	9	view_user
37	Can add doctor info	10	add_doctorinfo
38	Can change doctor info	10	change_doctorinfo
39	Can delete doctor info	10	delete_doctorinfo
40	Can view doctor info	10	view_doctorinfo
41	Can add user ip	11	add_userip
42	Can change user ip	11	change_userip
43	Can delete user ip	11	delete_userip
44	Can view user ip	11	view_userip
45	Can add pharmacy info	12	add_pharmacyinfo
46	Can change pharmacy info	12	change_pharmacyinfo
47	Can delete pharmacy info	12	delete_pharmacyinfo
48	Can view pharmacy info	12	view_pharmacyinfo
49	Can add patient info	13	add_patientinfo
50	Can change patient info	13	change_patientinfo
51	Can delete patient info	13	delete_patientinfo
52	Can view patient info	13	view_patientinfo
53	Can add doctor specialty	14	add_doctorspecialty
54	Can change doctor specialty	14	change_doctorspecialty
55	Can delete doctor specialty	14	delete_doctorspecialty
56	Can view doctor specialty	14	view_doctorspecialty
57	Can add doctor review	15	add_doctorreview
58	Can change doctor review	15	change_doctorreview
59	Can delete doctor review	15	delete_doctorreview
60	Can view doctor review	15	view_doctorreview
61	Can add doctor language	16	add_doctorlanguage
62	Can change doctor language	16	change_doctorlanguage
63	Can delete doctor language	16	delete_doctorlanguage
64	Can view doctor language	16	view_doctorlanguage
65	Can add doctor experience	17	add_doctorexperience
66	Can change doctor experience	17	change_doctorexperience
67	Can delete doctor experience	17	delete_doctorexperience
68	Can view doctor experience	17	view_doctorexperience
69	Can add doctor education	18	add_doctoreducation
70	Can change doctor education	18	change_doctoreducation
71	Can delete doctor education	18	delete_doctoreducation
72	Can view doctor education	18	view_doctoreducation
73	Can add doctor available hours	19	add_doctoravailablehours
74	Can change doctor available hours	19	change_doctoravailablehours
75	Can delete doctor available hours	19	delete_doctoravailablehours
76	Can view doctor available hours	19	view_doctoravailablehours
77	Can add clinic info	20	add_clinicinfo
78	Can change clinic info	20	change_clinicinfo
79	Can delete clinic info	20	delete_clinicinfo
80	Can view clinic info	20	view_clinicinfo
81	Can add password reset whitelist	21	add_passwordresetwhitelist
82	Can change password reset whitelist	21	change_passwordresetwhitelist
83	Can delete password reset whitelist	21	delete_passwordresetwhitelist
84	Can view password reset whitelist	21	view_passwordresetwhitelist
85	Can add doctor accepted insurance	22	add_doctoracceptedinsurance
86	Can change doctor accepted insurance	22	change_doctoracceptedinsurance
87	Can delete doctor accepted insurance	22	delete_doctoracceptedinsurance
88	Can view doctor accepted insurance	22	view_doctoracceptedinsurance
89	Can add waiting room	23	add_waitingroom
90	Can change waiting room	23	change_waitingroom
91	Can delete waiting room	23	delete_waitingroom
92	Can view waiting room	23	view_waitingroom
93	Can add patient encounters	24	add_patientencounters
94	Can change patient encounters	24	change_patientencounters
95	Can delete patient encounters	24	delete_patientencounters
96	Can view patient encounters	24	view_patientencounters
97	Can add assessment diagnosis	25	add_assessmentdiagnosis
98	Can change assessment diagnosis	25	change_assessmentdiagnosis
99	Can delete assessment diagnosis	25	delete_assessmentdiagnosis
100	Can view assessment diagnosis	25	view_assessmentdiagnosis
101	Can add patient social history	26	add_patientsocialhistory
102	Can change patient social history	26	change_patientsocialhistory
103	Can delete patient social history	26	delete_patientsocialhistory
104	Can view patient social history	26	view_patientsocialhistory
105	Can add plan of care	27	add_planofcare
106	Can change plan of care	27	change_planofcare
107	Can delete plan of care	27	delete_planofcare
108	Can view plan of care	27	view_planofcare
109	Can add ic ds	28	add_icds
110	Can change ic ds	28	change_icds
111	Can delete ic ds	28	delete_icds
112	Can view ic ds	28	view_icds
113	Can add patient procedure	29	add_patientprocedure
114	Can change patient procedure	29	change_patientprocedure
115	Can delete patient procedure	29	delete_patientprocedure
116	Can view patient procedure	29	view_patientprocedure
117	Can add functional and cognitive status	30	add_functionalandcognitivestatus
118	Can change functional and cognitive status	30	change_functionalandcognitivestatus
119	Can delete functional and cognitive status	30	delete_functionalandcognitivestatus
120	Can view functional and cognitive status	30	view_functionalandcognitivestatus
121	Can add chief complaints and hpi	31	add_chiefcomplaintsandhpi
122	Can change chief complaints and hpi	31	change_chiefcomplaintsandhpi
123	Can delete chief complaints and hpi	31	delete_chiefcomplaintsandhpi
124	Can view chief complaints and hpi	31	view_chiefcomplaintsandhpi
125	Can add vitals	32	add_vitals
126	Can change vitals	32	change_vitals
127	Can delete vitals	32	delete_vitals
128	Can view vitals	32	view_vitals
129	Can add review of system	33	add_reviewofsystem
130	Can change review of system	33	change_reviewofsystem
131	Can delete review of system	33	delete_reviewofsystem
132	Can view review of system	33	view_reviewofsystem
133	Can add physical exam	34	add_physicalexam
134	Can change physical exam	34	change_physicalexam
135	Can delete physical exam	34	delete_physicalexam
136	Can view physical exam	34	view_physicalexam
137	Can add orders	35	add_orders
138	Can change orders	35	change_orders
139	Can delete orders	35	delete_orders
140	Can view orders	35	view_orders
141	Can add appointment	36	add_appointment
142	Can change appointment	36	change_appointment
143	Can delete appointment	36	delete_appointment
144	Can view appointment	36	view_appointment
145	Can add inbox channel	37	add_inboxchannel
146	Can change inbox channel	37	change_inboxchannel
147	Can delete inbox channel	37	delete_inboxchannel
148	Can view inbox channel	37	view_inboxchannel
149	Can add inbox message	38	add_inboxmessage
150	Can change inbox message	38	change_inboxmessage
151	Can delete inbox message	38	delete_inboxmessage
152	Can view inbox message	38	view_inboxmessage
\.


--
-- Data for Name: authtoken_token; Type: TABLE DATA; Schema: public; Owner: sihan
--

COPY public.authtoken_token (key, created, user_id) FROM stdin;
383554340081f9e0b4c4b26f2a6cacce0caae981	2021-11-27 06:55:37.025521+00	2a2c60f1-e068-47d2-be66-88bd52116d20
f487af2dd74a4c8fcfaacbc549f4efe582e6899f	2021-11-27 06:57:28.819665+00	876b4dde-d1f6-4e79-a513-b7375b2b954c
f180a8755e95d75e8438ddef56809a6d59bcd910	2021-11-27 06:58:05.605579+00	ed76b722-e7f8-46cd-8dff-f4f687856bf3
b0afe24c60f6b5b2bc1fa31994036e81ea778a5a	2021-11-27 07:06:04.43744+00	09a95982-a373-4555-9347-b963628701ac
ddb8b66e47d2f9ae92357cb168f3bedcde5c5f58	2021-11-27 07:07:11.425912+00	1dd1ffe0-2113-4c97-bcf2-abe2798bba3d
055353d501a00aa5a0e93a690abd985e1d61e58f	2021-11-27 07:11:49.288393+00	3a0edd9f-747f-4c4d-b271-bc6b38696fe4
73be292a9ea01fe42e7c134aa7aed5e6d896470c	2021-11-27 07:27:20.472673+00	b082a946-48ab-4391-84f6-3892814e0f3a
70ff036aa9f2e6946efd5dbd80be9d1a8004c18d	2021-11-27 08:26:59.410291+00	77ffd331-ced9-46e1-947c-d445565eecce
d4fa81c8598596c1f284c291e593264c8755faac	2021-11-28 02:51:37.285641+00	4dfe08bf-0e1a-41a5-9e25-02c0ad512c4b
c0642c90ddb4154e9a31dba4920c7e072d8a7c02	2021-11-28 02:53:56.984862+00	e5bbcb5a-deef-46d5-9226-1fbb9b7398c8
572dec3f1864a31b24680b4bf7365a70153ab1d7	2021-11-28 08:15:39.206953+00	c5ce351d-b516-4a27-b62a-30eb1ec98025
27529bf304f371a4ec249bd3657fba7694e141ce	2021-11-29 05:26:53.780143+00	17e97df5-162c-45ec-a190-79626b980f4b
3ade2894eb0b7b981fe056b37ba477bb8d9279fa	2021-11-29 08:27:24.693026+00	f0eb657a-57e3-4d10-b336-8523c5a02050
21ec25607c158b684d28e7590092e670df66b13e	2021-11-30 05:37:58.817658+00	633420fb-e20c-4deb-8162-bedcd3d92c68
da6a301a7d35cacd301b3a030871b1659c4477f8	2021-11-30 05:39:51.792498+00	c739b88f-ffa9-4e03-9a5f-f9064b472b65
f7241d77cba5a22030971fda1a242a61ff796972	2021-11-30 05:43:58.230212+00	c1f9bc20-8e97-4e7a-b2a1-2419ede06191
07ce69b43448ec13c5087f49ed424bc84cce5a3b	2021-11-30 05:46:33.420052+00	bddf4b1e-3a5b-4f13-a89f-c43b79d9cfde
774e863ba08cd97d82e718744717a0455477aba8	2021-11-30 05:49:10.122791+00	245b2b72-4fae-40ac-bab1-f3cfc0f70c42
7a85210e6c916e53ca0f1f163667a1c9a15fab52	2021-11-30 05:53:33.779332+00	91d1b59d-b202-486a-bfcc-d9c0490a88f7
ec8dece46682f69fc6ce0677aff112c1d8705bbd	2021-11-30 06:33:35.90943+00	dd7346c1-32db-48dd-8274-c4eca960836c
44f6848453bd1ee09a01ba7fc138be60838ef2e8	2021-11-30 06:45:09.263863+00	88efdf2d-bec2-4221-9196-a11ef2391bd3
e6c62eae8ec69b003fe64280f89c1c8fe03b9b3c	2021-11-30 06:47:33.964494+00	a2d0ca75-c7b0-4ccd-bdcb-9fcfd76db504
5a58e1c51c02710da13e574a99bcbe81754cd438	2021-11-30 06:50:53.438607+00	cbff03a1-de8f-4f06-be55-6689d56b5c91
00db2d82af9295d70bc1c7073d0ffb86c5a335b6	2021-11-30 06:53:37.31439+00	8c268125-2199-4272-ad77-6e857678702a
3ec63286ea1ee97be134a18526d409a0db89b8ad	2021-11-30 06:57:05.252623+00	75a74960-1352-4fc4-97a8-eba612426c7c
5913d8dec04ba5cf6578996b3b51eafad7772bc0	2021-11-30 08:02:18.596326+00	4ebfc00b-4b4a-442a-b135-782bcc6b112e
a897c631aeaf8022c78c2be15bbcf4fdc068ad6f	2021-11-30 08:05:26.201826+00	35c8c822-025c-4342-8fb0-424af92b2cc8
fc3b2fec259e6ebffdd7d0eeaec77bed96d03244	2021-11-30 08:22:23.517815+00	1c2c6aa1-90b0-475a-a95a-6d396e0f2bda
180ad589407f73fb721940d8e11565419a08e14e	2021-11-30 11:43:25.789065+00	a81869fe-3d7e-4a82-b9a7-239311c5c5a2
9745558fabfec6ae93368d3ba823cd98c471a057	2021-11-30 12:32:09.660588+00	b92072ba-b707-4da1-89bc-0c16e4b65634
3030caa6f98e2b3d913a3100ad43801fb8df0a14	2021-12-01 00:19:20.809758+00	554b90e7-9846-4d91-baec-c5848702fb26
af9eb8621759c583391bb958ac88c088661feb48	2021-12-01 00:20:45.236184+00	969142a9-3a26-45f1-952e-6ec5d0e6fa1a
64619b64ec43f6ad39e3a09dce287fd3f1ab7041	2021-12-01 08:16:41.948904+00	4fd98941-ef2f-4812-b7e1-3b707fb6140c
e9d21e35203a734964b624c9081003958c605d87	2021-12-02 04:36:12.610509+00	b800d6d5-deb5-4e73-806a-1a85070662f2
09688852b0aa8f2d53f2853ca0f17e97a803f152	2021-12-03 06:14:05.748928+00	ed504b9b-7ed0-403a-b26b-003cbbad9b36
d0e5a7d26057bcf2ff480692f6084e3cde0e9a1b	2021-12-03 06:15:46.60801+00	977bbe34-1fd2-435b-b1f5-bf90d363f34f
41b97c0624245e93402a3efa673f1284b66c706f	2021-12-03 06:23:31.815225+00	1dc9b5f7-ef76-4c5f-9986-27f8eb721295
9326a32bc23fb54e7dca1b6c3bdeeb340be775a8	2021-12-03 06:28:04.128963+00	7d634e50-e284-4ecd-a54d-889bd138223c
bca81c4b731e518fadec3f91248effa09a9b6aa1	2021-12-03 06:30:21.934562+00	27911350-88bb-43ff-85c6-d0347936563e
4c84f7af87755c1cc0df779f9bc0482bd4d0252d	2021-12-03 07:06:35.176386+00	a91af88c-fc35-46b5-8831-5e23c00abbbc
b076b6e34874fa65ef7bf9ad565075662ba740d6	2021-12-03 07:09:08.067031+00	69563331-2401-4acb-98e3-4089f7298f45
1fe8643c5ee0721f77572d1990e3898ee531a798	2021-12-03 08:55:39.040116+00	49dbba2e-f487-4c5c-aa4b-3964d34b6711
cf1960b4bcb33da6c76d6d48e1bd6219b43fb21b	2021-12-03 10:25:47.348711+00	10210419-bb1d-4192-af63-77fc3b86fa4a
b819f7c2bb33c75a52b3f58b1f11d6b15214708a	2021-12-03 10:35:19.672333+00	b75bc244-cd62-4d39-b257-2820aa43eeb8
0a42842fb37e4d7aba82da6c07b771e937f85359	2021-12-03 10:37:14.063484+00	81a1c762-0527-457c-88f4-ac0dd02e870d
4885d81d9478534ce1a7c53b9769c73bc3c2152e	2021-12-03 10:38:31.564225+00	b8c2953f-2b6b-4407-a54c-7416f78541e9
00f8d4473e4c90e84325e3a258e92c08a973b1ee	2021-12-03 13:50:07.477269+00	f7eb6b06-45b4-4b44-afd0-2544d3284303
2bda70b23e36d4e3cf45de8b6c7b804b2a8f67b2	2021-12-04 17:37:51.434232+00	7765be45-f16d-41a0-b1a1-24498b59eeac
293f1e898ff59885a6c9abfb1c01b4aa54848127	2021-12-04 17:42:51.204496+00	5faf1dc6-fa78-4082-b4a6-8b2a00cd715d
bb3081a36b19742bc1e42c95ae7429bec6f9fe74	2021-12-07 03:06:01.189307+00	c815552a-0f4b-48da-a871-f86a4ed15268
b18b7f58d4aca7d54ca6cd2ef9e96274de81a113	2021-12-07 12:52:55.731668+00	64f65ba5-7d1d-4bfb-a54a-cb94b271e652
bbf8d5daf98a9cc29efaa228cdbecdbcb2bdc61c	2021-12-08 04:49:01.999965+00	89a45785-8ce9-4605-b28a-e123a7c47025
91f4a7a27816444f9d83b81df6eec42e1a15e6cf	2021-12-08 04:58:10.614491+00	53f3d1ab-6ef4-423f-abbe-2f502d021ac0
fc94a1d928d7e25249d301aa7222239a03b79d47	2021-12-08 05:30:57.903221+00	3beb642d-d876-4d39-8539-8efb9def2622
941b62fc95f58cc1fff7e36c214e975c30a8caa7	2021-12-08 05:35:18.37418+00	74096425-92ab-49d7-ad1a-c35b355e3260
472a7da406ca7770040bbd01c922f6ce8ac44f51	2021-12-09 10:02:09.627469+00	5d454090-2584-4953-852c-c6a0e2c2d30e
4f6f888214fb581802fdac2c04914079e826123e	2021-12-09 13:15:22.464553+00	fbfe7a13-6ef7-4094-b211-6407aeeb1f30
bcc58b40e21408527e8fdacbff95e91777ed8306	2021-12-10 04:42:43.107573+00	fc8297cd-9b86-4033-a97e-da5abe71d76f
2764b550491b3e7ad1789816a3d50e6448c93bed	2021-12-10 04:45:23.563286+00	74df4c91-61c9-4d1f-8c5e-05fef52eecf9
c8fa3f4cceb2f3cf61b68f537c867e475b780a6d	2021-12-10 14:53:02.487076+00	a0312245-e73a-4763-9a27-5a2aba93cda3
6bbdab1c6aba85ed8e02b7d99a85fbbe59fd53b2	2021-12-10 15:34:28.764458+00	bddc3d89-087a-4ff0-9101-58ff4633bf74
063c8e41fa1d1cf77631696a5c7bf07b71ce152e	2021-12-14 08:47:25.8045+00	235a9a51-9ceb-4b55-a687-46bc634eb0fa
26c0860c54f57875e1b07d309b008876438c804c	2021-12-14 17:02:16.548269+00	70b8af3e-d59d-48e7-90e6-ded64489cf7f
7b4a6300b8f9e099f5cbb2991eb15501675e5483	2021-12-14 19:19:17.121705+00	db3fc55b-bd76-4ce6-9874-170ab76870ca
76702be0b2fb899cdecd9ee2be38424dc67f2a1d	2021-12-15 07:24:55.534612+00	2c32724e-8565-4a35-84d7-430b411c83be
2f19ebc7b0de4f441f2a217f7d7ea9b4eb41a8ad	2021-12-15 07:30:08.985505+00	121f7441-6453-455e-ab9c-4b50a64ecf66
1ea42d3ef527c52e83f06b36945b4a933f774814	2021-12-17 06:54:48.998134+00	03f1a586-fb3e-4480-8d04-9273bb383245
9c3f94e31793021e112206ba8b1a68e3b56a024e	2021-12-17 16:00:16.415756+00	1d5b7522-c466-4bec-85f4-943ee6ae16c6
9915a449aefabac1b5eba534d00dd6072aa0c9f1	2021-12-20 08:26:15.992127+00	e7556c15-90eb-42ab-b45c-0ab6cf333068
c310df1a2f402a6756b247d49717975992b0de8e	2021-12-20 22:30:42.204145+00	881eb97b-ce35-4df5-8aaf-0c688c34f00c
af6d6776830b0e8e2ad67504e8bcbedc38d8aedf	2021-12-22 06:22:49.683923+00	7c52ea4a-efb3-4d4e-804f-e9bd2049cafa
6872ea9657d170557c980de8be0f0410876cad45	2021-12-22 08:27:03.530749+00	0f219fd8-c6b7-4823-a783-b0900d6743ab
c46b2bd91a900bb14d542d77fdd3247437087589	2021-12-22 10:18:16.247511+00	8bf64794-80d0-4d64-bfc3-8a167f4f8960
97a88d079b8b35336e5eed9847c410aa1f02c36d	2021-12-23 05:34:36.73207+00	76d927d5-9b1d-4418-badd-a970cbf72c88
8f05e913c4831a39fc734896dd656bc753c9bb6c	2021-12-24 05:15:39.985608+00	444d8a39-22e2-4544-a261-0ec6fc70215c
d1c6c9f4f3d8e3c87354041ce19e266b15742234	2021-12-25 10:18:45.831498+00	6c0e20bd-57f4-48e6-a2bf-75319fef2cf3
9b25a8ac6edec77c1e0ebad45e69466c3c247899	2021-12-27 07:21:14.660729+00	f23ba24b-665e-4e01-8b9a-85cda57e4ad1
21116d4996676e2829cf687c8a4345c23d386b66	2021-12-27 07:22:28.927882+00	952478f7-4c6e-497a-b6c0-7f11ca93ae12
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: sihan
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2021-12-04 00:27:08.3566+00	a9693260-afc6-49d7-9292-eb6bc3a6da49	shafayathossainkhan@gmail.com	3		9	25482094-6737-4177-b465-9a179fd5602d
2	2021-12-04 00:27:08.360467+00	1aa8826a-0634-4abc-b47a-d4079679ee21	shafayathossainkhan3@gmail.com	3		9	25482094-6737-4177-b465-9a179fd5602d
3	2021-12-04 17:36:16.775183+00	22123f99-6f67-4c3c-b330-3e0592482f46	patientshafayat@gmail.com	3		9	25482094-6737-4177-b465-9a179fd5602d
4	2021-12-07 12:27:43.180366+00	4fb7958b-94e4-4354-a641-3023a788ccc1	4fb7958b-94e4-4354-a641-3023a788ccc1-mahmudul	2	[{"changed": {"fields": ["Professional bio"]}}]	10	25482094-6737-4177-b465-9a179fd5602d
5	2021-12-07 12:40:44.751279+00	952478f7-4c6e-497a-b6c0-7f11ca93ae12	mahmudul	2	[{"changed": {"fields": ["Full name"]}}]	9	25482094-6737-4177-b465-9a179fd5602d
6	2021-12-07 12:41:45.153607+00	4fb7958b-94e4-4354-a641-3023a788ccc1	4fb7958b-94e4-4354-a641-3023a788ccc1-mahmudul	2	[{"changed": {"fields": ["Professional bio"]}}]	10	25482094-6737-4177-b465-9a179fd5602d
7	2021-12-07 12:44:17.190851+00	952478f7-4c6e-497a-b6c0-7f11ca93ae12	mahmudul	2	[{"changed": {"fields": ["Email"]}}]	9	25482094-6737-4177-b465-9a179fd5602d
8	2021-12-07 12:44:41.184824+00	952478f7-4c6e-497a-b6c0-7f11ca93ae12	mahmudul	2	[{"changed": {"fields": ["Email"]}}]	9	25482094-6737-4177-b465-9a179fd5602d
9	2021-12-07 12:50:55.077663+00	952478f7-4c6e-497a-b6c0-7f11ca93ae12	mahmudul	2	[{"changed": {"fields": ["Email"]}}]	9	25482094-6737-4177-b465-9a179fd5602d
10	2021-12-07 13:11:08.484659+00	bbf9b545-a1ac-487a-a960-ddee8d9b18f0	bbf9b545-a1ac-487a-a960-ddee8d9b18f0	1	[{"added": {}}]	18	25482094-6737-4177-b465-9a179fd5602d
11	2021-12-07 13:13:12.60286+00	ea7e513f-065f-44e6-916e-717f5f378294	ea7e513f-065f-44e6-916e-717f5f378294	3		18	25482094-6737-4177-b465-9a179fd5602d
12	2021-12-07 13:13:28.687897+00	bbf9b545-a1ac-487a-a960-ddee8d9b18f0	bbf9b545-a1ac-487a-a960-ddee8d9b18f0	2	[{"changed": {"fields": ["Year"]}}]	18	25482094-6737-4177-b465-9a179fd5602d
13	2021-12-07 13:14:42.83358+00	a24068ba-2aa3-4c4e-aa8f-492892c5e655	a24068ba-2aa3-4c4e-aa8f-492892c5e655	3		18	25482094-6737-4177-b465-9a179fd5602d
14	2021-12-07 13:18:45.01851+00	1e3bd713-d981-44fb-aae4-33732b784e2d	1e3bd713-d981-44fb-aae4-33732b784e2d	1	[{"added": {}}]	17	25482094-6737-4177-b465-9a179fd5602d
15	2021-12-07 13:19:10.457367+00	eb2618d9-4f7d-4c2d-8ebe-d06103849bc9	eb2618d9-4f7d-4c2d-8ebe-d06103849bc9	3		17	25482094-6737-4177-b465-9a179fd5602d
16	2021-12-07 13:19:33.349053+00	1e3bd713-d981-44fb-aae4-33732b784e2d	1e3bd713-d981-44fb-aae4-33732b784e2d	2	[{"changed": {"fields": ["End date"]}}]	17	25482094-6737-4177-b465-9a179fd5602d
17	2021-12-11 07:46:09.96+00	09a95982-a373-4555-9347-b963628701ac	sanviraj.zahin.haque	2	[{"changed": {"fields": ["Active"]}}]	9	25482094-6737-4177-b465-9a179fd5602d
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: sihan
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	contenttypes	contenttype
5	sessions	session
6	sites	site
7	authtoken	token
8	authtoken	tokenproxy
9	user	user
10	user	doctorinfo
11	user	userip
12	user	pharmacyinfo
13	user	patientinfo
14	user	doctorspecialty
15	user	doctorreview
16	user	doctorlanguage
17	user	doctorexperience
18	user	doctoreducation
19	user	doctoravailablehours
20	user	clinicinfo
21	user	passwordresetwhitelist
22	user	doctoracceptedinsurance
23	twilio_chat	waitingroom
24	ehr	patientencounters
25	ehr	assessmentdiagnosis
26	ehr	patientsocialhistory
27	ehr	planofcare
28	ehr	icds
29	ehr	patientprocedure
30	ehr	functionalandcognitivestatus
31	ehr	chiefcomplaintsandhpi
32	ehr	vitals
33	ehr	reviewofsystem
34	ehr	physicalexam
35	ehr	orders
36	appointment	appointment
37	inbox	inboxchannel
38	inbox	inboxmessage
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: sihan
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2021-12-27 16:01:17.941517+00
2	contenttypes	0002_remove_content_type_name	2021-12-27 16:01:17.947114+00
3	auth	0001_initial	2021-12-27 16:01:17.995619+00
4	auth	0002_alter_permission_name_max_length	2021-12-27 16:01:18.001323+00
5	auth	0003_alter_user_email_max_length	2021-12-27 16:01:18.006922+00
6	auth	0004_alter_user_username_opts	2021-12-27 16:01:18.011396+00
7	auth	0005_alter_user_last_login_null	2021-12-27 16:01:18.015959+00
8	auth	0006_require_contenttypes_0002	2021-12-27 16:01:18.01851+00
9	auth	0007_alter_validators_add_error_messages	2021-12-27 16:01:18.025889+00
10	auth	0008_alter_user_username_max_length	2021-12-27 16:01:18.033657+00
11	auth	0009_alter_user_last_name_max_length	2021-12-27 16:01:18.040426+00
12	auth	0010_alter_group_name_max_length	2021-12-27 16:01:18.047209+00
13	auth	0011_update_proxy_permissions	2021-12-27 16:01:18.053635+00
14	auth	0012_alter_user_first_name_max_length	2021-12-27 16:01:18.060623+00
15	user	0001_initial	2021-12-27 16:01:18.334855+00
16	admin	0001_initial	2021-12-27 16:01:18.371563+00
17	admin	0002_logentry_remove_auto_add	2021-12-27 16:01:18.385446+00
18	admin	0003_logentry_add_action_flag_choices	2021-12-27 16:01:18.39977+00
19	appointment	0001_initial	2021-12-27 16:01:18.439257+00
20	appointment	0002_alter_appointment_patient	2021-12-27 16:01:18.470885+00
21	authtoken	0001_initial	2021-12-27 16:01:18.505192+00
22	authtoken	0002_auto_20160226_1747	2021-12-27 16:01:18.550852+00
23	authtoken	0003_tokenproxy	2021-12-27 16:01:18.554303+00
24	ehr	0001_initial	2021-12-27 16:01:18.646265+00
25	ehr	0002_patientsocialhistory	2021-12-27 16:01:18.684193+00
26	ehr	0003_auto_20211204_0023	2021-12-27 16:01:18.725462+00
27	ehr	0004_icds	2021-12-27 16:01:18.73731+00
28	ehr	0005_chiefcomplaintsandhpi_functionalandcognitivestatus_patientprocedure	2021-12-27 16:01:18.846178+00
29	ehr	0006_rename_type_patientprocedure_procedure_type	2021-12-27 16:01:18.855292+00
30	ehr	0007_auto_20211210_0811	2021-12-27 16:01:18.901603+00
31	ehr	0008_auto_20211222_1908	2021-12-27 16:01:19.006966+00
32	ehr	0009_patientencounters_timing	2021-12-27 16:01:19.026427+00
33	inbox	0001_initial	2021-12-27 16:01:19.088398+00
34	inbox	0002_alter_inboxmessage_channel	2021-12-27 16:01:19.111684+00
35	sessions	0001_initial	2021-12-27 16:01:19.130712+00
36	sites	0001_initial	2021-12-27 16:01:19.139312+00
37	sites	0002_alter_domain_unique	2021-12-27 16:01:19.151271+00
38	user	0002_patientinfo_display_id	2021-12-27 16:01:19.169774+00
39	user	0003_doctorinfo_profession	2021-12-27 16:01:19.190749+00
40	user	0004_passwordresetwhitelist	2021-12-27 16:01:19.21569+00
41	twilio_chat	0001_initial	2021-12-27 16:01:19.243401+00
42	twilio_chat	0002_waitingroom_room_media_mime_type	2021-12-27 16:01:19.295172+00
43	twilio_chat	0003_alter_waitingroom_room_media_mime_type	2021-12-27 16:01:19.304174+00
44	user	0005_doctoracceptedinsurance	2021-12-27 16:01:19.331966+00
45	user	0006_doctorinfo_license_expiration	2021-12-27 16:01:19.346014+00
46	user	0007_auto_20211217_1755	2021-12-27 16:01:19.371403+00
47	user	0008_clinicinfo_website	2021-12-27 16:01:19.385515+00
48	user	0009_auto_20211223_0843	2021-12-27 16:01:19.402367+00
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: sihan
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
xx8n3poz006p19fvdodefrl4k6nkzf4t	.eJxVjEsOgzAMBe-SdYkCjmOny-57BhTHofQjkPisqt69ILFol08z896mTevSt-tcpvau5mwa9Ny46KtAQJWviSrxAauYaoqdYnCNmtNvJik_y7C3-kjDbbR5HJbpLnZX7EFnex21vC6H-3fQp7nf6o4DYMKidcYSMwN6AFTAKNtGdUggQTMLxFCIJfroiJ1oYHYlm88XCk4_cw:1mrKfa:fxs2dje_t8mMUA81DvE9476rXutz_WOuFW13ytK7FwQ	2021-12-12 07:56:42.300393+00
4qmwq98i5tlh565wxsrjeao7hpji5ni1	.eJxVjEsOgzAMBe-SdYkCjmOny-57BhTHofQjkPisqt69ILFol08z896mTevSt-tcpvau5mwa9Ny46KtAQJWviSrxAauYaoqdYnCNmtNvJik_y7C3-kjDbbR5HJbpLnZX7EFnex21vC6H-3fQp7nf6o4DYMKidcYSMwN6AFTAKNtGdUggQTMLxFCIJfroiJ1oYHYlm88XCk4_cw:1msPB2:FX2m5uIumMue8INJviPASKA2x9d_K0WG-nfo_BdIz4o	2021-12-15 06:57:36.971093+00
22oye8xbt6302xw6zp2c6mu78d9zkvw0	.eJxVjEsOgzAMBe-SdYkCjmOny-57BhTHofQjkPisqt69ILFol08z896mTevSt-tcpvau5mwa9Ny46KtAQJWviSrxAauYaoqdYnCNmtNvJik_y7C3-kjDbbR5HJbpLnZX7EFnex21vC6H-3fQp7nf6o4DYMKidcYSMwN6AFTAKNtGdUggQTMLxFCIJfroiJ1oYHYlm88XCk4_cw:1mtOUz:cuilZmQzIQCWOHFm5WBaIa_DKF1y_83iUhNTTxJhFN8	2021-12-18 00:26:17.312899+00
0gy6olofrmdj2qryoh3bcpd47zlrxqia	.eJxVjEsOgzAMBe-SdYkCjmOny-57BhTHofQjkPisqt69ILFol08z896mTevSt-tcpvau5mwa9Ny46KtAQJWviSrxAauYaoqdYnCNmtNvJik_y7C3-kjDbbR5HJbpLnZX7EFnex21vC6H-3fQp7nf6o4DYMKidcYSMwN6AFTAKNtGdUggQTMLxFCIJfroiJ1oYHYlm88XCk4_cw:1muf9i:R3bd0ZvvrTnfOrx-Oi8Wzlvx-SxDbWmU07e2TGTYgF0	2021-12-21 12:25:34.029207+00
9543ssnaqt3m884qmadgwen9wk1h3n6r	.eJxVjEsOgzAMBe-SdYkCjmOny-57BhTHofQjkPisqt69ILFol08z896mTevSt-tcpvau5mwa9Ny46KtAQJWviSrxAauYaoqdYnCNmtNvJik_y7C3-kjDbbR5HJbpLnZX7EFnex21vC6H-3fQp7nf6o4DYMKidcYSMwN6AFTAKNtGdUggQTMLxFCIJfroiJ1oYHYlm88XCk4_cw:1mxVCo:gFpuRPoskJb4MPZjEsSy1uN0LIUwbsgVuPBn7aZlXFE	2021-12-29 08:24:30.506069+00
3fx81a3nej0kf68joy80v50zop55rl5p	.eJxVjEsOgzAMBe-SdYkCjmOny-57BhTHofQjkPisqt69ILFol08z896mTevSt-tcpvau5mwa9Ny46KtAQJWviSrxAauYaoqdYnCNmtNvJik_y7C3-kjDbbR5HJbpLnZX7EFnex21vC6H-3fQp7nf6o4DYMKidcYSMwN6AFTAKNtGdUggQTMLxFCIJfroiJ1oYHYlm88XCk4_cw:1mzNtZ:cXfRmykU0ts5-vTo91DCySYciDjgwS1Ncit3-Hloof0	2022-01-03 13:00:25.968364+00
sngiezll33qjhj9lt90pf7lb5rarsn01	.eJxVjEsOgzAMBe-SdYkCjmOny-57BhTHofQjkPisqt69ILFol08z896mTevSt-tcpvau5mwa9Ny46KtAQJWviSrxAauYaoqdYnCNmtNvJik_y7C3-kjDbbR5HJbpLnZX7EFnex21vC6H-3fQp7nf6o4DYMKidcYSMwN6AFTAKNtGdUggQTMLxFCIJfroiJ1oYHYlm88XCk4_cw:1mzNzE:Vw6F7kglA7pTuKS8BaAhI64RdVItTzPgm7llnuElkd4	2022-01-03 13:06:16.745422+00
\.


--
-- Data for Name: django_site; Type: TABLE DATA; Schema: public; Owner: sihan
--

COPY public.django_site (id, domain, name) FROM stdin;
1	http://20.122.232.244	dokto
\.


--
-- Data for Name: ehr_assessmentdiagnosis; Type: TABLE DATA; Schema: public; Owner: sihan
--

COPY public.ehr_assessmentdiagnosis (id, created_at, updated_at, is_deleted, deleted_at, icd, icd_description, disease_code, disease_description, disease_name, start_date, end_date, diagnosis_type, primary_diagnosis, assessment, patient_encounter_id) FROM stdin;
17025339-0726-40d1-9dd6-516c1089c5e6	2021-12-15 11:45:54.248993+00	2021-12-15 11:45:54.249056+00	t	2021-12-15 11:41:34.345+00	string	string	string	string	string	2021-12-15	2021-12-15	ACUTE	t	string	9d36d544-2461-4abf-aaf6-188566879888
\.


--
-- Data for Name: ehr_chiefcomplaintsandhpi; Type: TABLE DATA; Schema: public; Owner: sihan
--

COPY public.ehr_chiefcomplaintsandhpi (id, created_at, updated_at, is_deleted, deleted_at, "chiefComplaint", location, severity, duration, modifying_factors, associated_symptons, description, context, hpi, patient_encounter_id, timing) FROM stdin;
4fc7d92a-ef18-4574-a037-63f1d3c8ff8d	2021-12-17 05:43:25.303729+00	2021-12-17 05:43:25.303778+00	t	2021-12-17 05:43:01.43+00	string	string	string	string	string	string	string	string	string	2e25724a-9018-499d-9250-eca8c7fd2a28	\N
b3364b1a-b625-4df6-a131-cde26270a274	2021-12-17 05:46:50.830117+00	2021-12-17 05:46:50.830156+00	f	\N	FEMALE	Dhaka	MALE	MALE	FEMALE	something	desc	hmm	\N	2e25724a-9018-499d-9250-eca8c7fd2a28	\N
45ee0a5f-0729-4f02-863c-9afd8e8e23da	2021-12-17 05:54:38.749415+00	2021-12-17 05:54:38.749451+00	f	\N	FEMALE	Dhaka	MALE	MALE	FEMALE	something	desc	hmm	\N	2e25724a-9018-499d-9250-eca8c7fd2a28	\N
d68ce452-55ec-46e4-9314-4c7208055e9e	2021-12-17 07:26:27.839845+00	2021-12-17 07:26:27.839888+00	f	\N	\N	\N	\N	\N	\N	\N	description	\N	\N	2e25724a-9018-499d-9250-eca8c7fd2a28	\N
908cb2cc-8e40-4896-8c44-613bc87a3ff4	2021-12-22 07:00:54.131838+00	2021-12-22 07:00:54.131875+00	f	\N	\N	\N	\N	\N	\N	\N	lalalalaa	\N	\N	7cb97c7b-b7c6-4f0e-b02b-93f5c0663006	\N
507fe32b-1b11-45ba-a782-bff771df7a25	2021-12-23 08:19:30.056625+00	2021-12-23 08:19:30.056671+00	f	\N	There is a complaint here	hek	Mild	1 year	idk	idk	NOTHING	WHO GIVES A	\N	7cb97c7b-b7c6-4f0e-b02b-93f5c0663006	what ?
779aff18-a0a7-4cb2-99de-3ddc749b6c72	2021-12-23 08:26:25.407004+00	2021-12-23 08:26:25.40704+00	f	\N	\N	\N	\N	\N	\N	\N	qweqweqwewqewqweqw	\N	\N	7cb97c7b-b7c6-4f0e-b02b-93f5c0663006	\N
6ef0eb23-e6bf-433e-814c-3c5f9dcacd8f	2021-12-23 08:28:28.365423+00	2021-12-23 08:28:28.365456+00	f	\N	There is a complaint here	hek	Mild	1 year	idk	idk	NOTHING	WHO GIVES A	\N	2e25724a-9018-499d-9250-eca8c7fd2a28	what ?
d696c7ba-0d9e-4b4c-b13c-3d14c6034e15	2021-12-23 08:43:38.068107+00	2021-12-23 08:43:38.068137+00	f	\N	hi	Dhaka	Mild	2.5h	Test	headache	desc	tester	\N	2e25724a-9018-499d-9250-eca8c7fd2a28	2.30pm
963a5ec5-f099-4baa-9f4f-0751611e7732	2021-12-23 08:48:24.896151+00	2021-12-23 08:48:24.896192+00	f	\N	There is a complaint here	hek	Moderate	1 year	idk	idk	NOTHING	WHO GIVES A	\N	9d36d544-2461-4abf-aaf6-188566879888	what ?
8cc093a6-690e-4f86-8cef-d95211eb9de9	2021-12-23 08:48:53.741305+00	2021-12-23 08:48:53.74134+00	f	\N	There is a complaint here	hek	Moderate	1 year	idk	idk	NOTHING	WHO GIVES A	\N	7cb97c7b-b7c6-4f0e-b02b-93f5c0663006	what ?
72e4de4c-5c71-4d9a-8396-0cf11582bda2	2021-12-23 08:51:23.215901+00	2021-12-23 08:51:23.215949+00	f	\N	\N	\N	\N	\N	\N	\N	desc	\N	\N	2e25724a-9018-499d-9250-eca8c7fd2a28	\N
\.


--
-- Data for Name: ehr_functionalandcognitivestatus; Type: TABLE DATA; Schema: public; Owner: sihan
--

COPY public.ehr_functionalandcognitivestatus (id, created_at, updated_at, is_deleted, deleted_at, "moduleType", "codeType", status, code, start_date, description, patient_encounter_id) FROM stdin;
e26696d6-800b-4712-a343-a2fb1554fd7a	2021-12-17 03:06:19.240741+00	2021-12-17 03:06:19.240778+00	t	2021-12-17 03:06:01.113+00	string	string	string	string	2021-12-17	string	2e25724a-9018-499d-9250-eca8c7fd2a28
2abe6a9f-4049-491f-a661-ccc369d41a60	2021-12-17 03:14:30.022287+00	2021-12-17 03:14:30.022403+00	f	\N	\N	\N	\N	\N	\N	\N	2e25724a-9018-499d-9250-eca8c7fd2a28
bcabb2e7-2b86-4fa0-bca0-cfb9a0f9c845	2021-12-17 03:19:20.880488+00	2021-12-17 03:19:20.880531+00	f	\N	MALE	FEMALE	FEMALE	871245	2021-12-10	\N	2e25724a-9018-499d-9250-eca8c7fd2a28
49fcb42f-957a-4aa4-9ce2-79ea45037e25	2021-12-17 03:24:27.700148+00	2021-12-17 03:24:27.700192+00	f	\N	MALE	MALE	FEMALE	871245	2021-12-04	hi there	2e25724a-9018-499d-9250-eca8c7fd2a28
7e849f66-64da-417e-ab04-6109bd248eed	2021-12-17 07:25:08.118226+00	2021-12-17 07:25:08.118282+00	f	\N	MALE	FEMALE	FEMALE	871245	2021-12-04	description	2e25724a-9018-499d-9250-eca8c7fd2a28
3b1f3372-c31b-4499-94f1-68b70df6d1cf	2021-12-22 06:54:31.896425+00	2021-12-22 06:54:31.896462+00	f	\N	Functional Status	ICD	InActive	undsad	2021-12-16	lalalalaa	7cb97c7b-b7c6-4f0e-b02b-93f5c0663006
cd1cd0ce-b6a8-42ca-b3e7-49dc3d5d38f5	2021-12-23 08:15:11.784668+00	2021-12-23 08:15:11.784706+00	f	\N	Functional Status	ICD	Active	undsad	2021-12-15	I need a docky	7cb97c7b-b7c6-4f0e-b02b-93f5c0663006
12c158a3-58f9-4510-8cd7-d7d37149bad1	2021-12-23 08:15:33.99499+00	2021-12-23 08:15:33.995037+00	f	\N	Functional Status	ICD	Active	undsad	2021-12-15	I need a docky	0c54acaf-99d8-48a6-aff3-1f9c695f5612
6abf8af5-fd31-4209-91bb-ca030932328c	2021-12-23 08:23:33.521226+00	2021-12-23 08:23:33.521278+00	f	\N	Functional Status	ICD	Inactive	undsad	2021-12-17	qweqweqwewqewqweqw	7cb97c7b-b7c6-4f0e-b02b-93f5c0663006
b1e26c14-c799-479e-97e3-a6ba171f149c	2021-12-23 08:45:45.133149+00	2021-12-23 08:45:45.133203+00	f	\N	Functional Status	ICD	Active	871245	2021-12-09	desc	2e25724a-9018-499d-9250-eca8c7fd2a28
658bd338-5d73-4ec2-bb85-0ff22d28b6b8	2021-12-23 08:50:07.233574+00	2021-12-23 08:50:07.233616+00	f	\N	Functional Status	ICD	Inactive	undsad	2021-12-15	aaaa	7cb97c7b-b7c6-4f0e-b02b-93f5c0663006
a7a41e5b-3ce7-4f49-93ff-92d1f17cc18d	2021-12-23 12:15:55.148972+00	2021-12-23 12:15:55.149014+00	f	\N	Functional Status	ICD	Active	undsad	2021-12-22	aaaa	7cb97c7b-b7c6-4f0e-b02b-93f5c0663006
\.


--
-- Data for Name: ehr_icds; Type: TABLE DATA; Schema: public; Owner: sihan
--

COPY public.ehr_icds (id, code_description, icd_code, full_description) FROM stdin;
\.


--
-- Data for Name: ehr_orders; Type: TABLE DATA; Schema: public; Owner: sihan
--

COPY public.ehr_orders (id, created_at, updated_at, is_deleted, deleted_at, lab_order, imaging_order, patient_encounter_id) FROM stdin;
\.


--
-- Data for Name: ehr_patientencounters; Type: TABLE DATA; Schema: public; Owner: sihan
--

COPY public.ehr_patientencounters (id, created_at, updated_at, is_deleted, deleted_at, visit_date, location, reason, signed, patient_id, provider_id, timing) FROM stdin;
2e25724a-9018-499d-9250-eca8c7fd2a28	2021-12-11 07:16:09.73112+00	2021-12-11 07:16:09.731173+00	t	2021-12-11 07:14:15.595+00	2021-12-11	string	string	t	a5e1d84b-6365-4d91-a62e-12f9d226a7ca	a354ca46-0d86-4f96-8cdb-590a8986513b	\N
7cb97c7b-b7c6-4f0e-b02b-93f5c0663006	2021-12-12 08:06:12.909043+00	2021-12-12 08:06:12.909084+00	t	2021-12-12 07:58:12.862+00	2021-12-12	string	string	t	b54ff328-3635-4084-a160-e1e98f65b47e	a354ca46-0d86-4f96-8cdb-590a8986513b	\N
9d36d544-2461-4abf-aaf6-188566879888	2021-12-12 08:06:26.220076+00	2021-12-12 08:06:26.220118+00	t	2021-12-12 07:58:12.862+00	2021-12-12	string	string	t	b54ff328-3635-4084-a160-e1e98f65b47e	a354ca46-0d86-4f96-8cdb-590a8986513b	\N
0c54acaf-99d8-48a6-aff3-1f9c695f5612	2021-12-12 08:06:33.846062+00	2021-12-12 08:06:33.846131+00	t	2021-12-12 07:58:12.862+00	2021-12-12	string	string	t	b54ff328-3635-4084-a160-e1e98f65b47e	a354ca46-0d86-4f96-8cdb-590a8986513b	\N
\.


--
-- Data for Name: ehr_patientprocedure; Type: TABLE DATA; Schema: public; Owner: sihan
--

COPY public.ehr_patientprocedure (id, created_at, updated_at, is_deleted, deleted_at, procedure_type, code, description, status, date, patient_encounter_id) FROM stdin;
ce05745e-d952-461e-ba1d-e455e49aa37d	2021-12-15 02:29:53.184673+00	2021-12-15 02:29:53.184708+00	f	\N	MALE	871245	hci	MALE	2021-12-04	9d36d544-2461-4abf-aaf6-188566879888
1dc02a97-afc1-4e0e-b24b-66cc6c947c98	2021-12-20 10:53:18.19299+00	2021-12-20 10:53:18.193075+00	f	\N	Chronic	631163	desc	Active	2021-12-17	2e25724a-9018-499d-9250-eca8c7fd2a28
8eb6b633-5403-4d5c-b2ea-d1c874c3b813	2021-12-20 19:13:14.944321+00	2021-12-20 19:13:14.944374+00	f	\N	Chronic	T674T	abcd	Active	2021-12-07	7cb97c7b-b7c6-4f0e-b02b-93f5c0663006
f4037c65-27b3-4a56-9b34-30fc8e741cc6	2021-12-21 00:07:57.256322+00	2021-12-21 00:07:57.256357+00	f	\N	Acute	631163	desc	Active	2021-12-10	2e25724a-9018-499d-9250-eca8c7fd2a28
18aa9d57-0761-4ccd-8903-c6afeae36c3f	2021-12-21 00:10:03.949901+00	2021-12-21 00:10:03.949954+00	f	\N	Chronic	397616	hci	Active	2021-12-09	2e25724a-9018-499d-9250-eca8c7fd2a28
ed0ef763-3bc2-47d3-9d32-def818b5b45a	2021-12-21 00:28:32.662591+00	2021-12-21 00:28:32.662638+00	f	\N	Chronic	631163	desc	Resolved	2021-12-11	2e25724a-9018-499d-9250-eca8c7fd2a28
e504159b-aefe-4551-b97b-963807de21bf	2021-12-21 00:31:02.735301+00	2021-12-21 00:31:02.735352+00	f	\N	Chronic	397616	hci	Active	2021-12-11	2e25724a-9018-499d-9250-eca8c7fd2a28
7ac64a20-88ab-4b99-b4d7-c8678b4aa83f	2021-12-23 08:20:07.630499+00	2021-12-23 08:20:07.630535+00	f	\N	\N	\N	\N	Active	2021-12-09	0c54acaf-99d8-48a6-aff3-1f9c695f5612
78072f3b-fc03-4347-8f44-ff7b8c40611e	2021-12-23 13:07:19.555507+00	2021-12-23 13:07:19.55554+00	f	\N	Acute	111	113123	Active	2021-12-25	9d36d544-2461-4abf-aaf6-188566879888
37890a2f-eb8a-4bf5-97e6-203304a5af4c	2021-12-23 13:07:36.877433+00	2021-12-23 13:07:36.877486+00	f	\N	Acute	111	113123	Active	2021-12-25	7cb97c7b-b7c6-4f0e-b02b-93f5c0663006
bde44edf-90ad-4870-8e3c-150152179896	2021-12-27 07:25:20.755951+00	2021-12-27 07:25:20.755984+00	f	\N	Chronic	233183	aaaa	Active	2021-12-07	7cb97c7b-b7c6-4f0e-b02b-93f5c0663006
\.


--
-- Data for Name: ehr_patientsocialhistory; Type: TABLE DATA; Schema: public; Owner: sihan
--

COPY public.ehr_patientsocialhistory (id, created_at, updated_at, is_deleted, deleted_at, home_environment, children, highest_education, occupation, sexual_orientation, gender_identity, tobacco_status, tobacco_type, tobacco_started_year, tobacco_packs_per_day, tobacco_start_date, tobacco_end_date, tobacco_cessation, exercise, drug_use, quit_date, seatbelts, exposure, alcohol_use, caffeine_use, etoh, patient_encounter_id, marital_status) FROM stdin;
72336d70-8dfb-4179-ab26-d555deee943b	2021-12-14 10:04:15.686626+00	2021-12-14 10:04:15.686679+00	f	\N	Assisted living	9	Middle School	hi	\N	Female-to-Male (FTM)/Transgender Male/Trans Man	Former smoker	Cigarette	\N	Half pack	2021-12-14	\N	2021-12-14	2-5 times/week	987	2021-12-30	2-5 times/week	Hepatitis	1-2 drinks/day	Never	Occasional	9d36d544-2461-4abf-aaf6-188566879888	hj
2222ae69-3a13-4502-b826-15e71a0a40cf	2021-12-14 10:04:30.466836+00	2021-12-14 10:04:30.466889+00	f	\N	Assisted living	9	Middle School	hi	\N	Female-to-Male (FTM)/Transgender Male/Trans Man	Former smoker	Cigarette	\N	Half pack	2021-12-14	\N	2021-12-14	2-5 times/week	987	2021-12-30	2-5 times/week	Hepatitis	1-2 drinks/day	Never	Occasional	9d36d544-2461-4abf-aaf6-188566879888	hj
c68f3e7a-fb54-43ef-81e2-bae9d80e3b7e	2021-12-14 10:24:24.190589+00	2021-12-14 10:24:24.190619+00	f	\N	apartment	9	Middle School	hi	\N	Female-to-Male (FTM)/Transgender Male/Trans Man	Former smoker	Chewing tobacco	\N	Less than 1 pack	2021-12-14	\N	2021-12-14	2-5 times/week	987	2021-12-06	Always	Hepatitis	Social drinker	Cigarette	Occasional	2e25724a-9018-499d-9250-eca8c7fd2a28	unmarried
73e14ea4-cdbf-4031-a634-8e291474d72a	2021-12-15 00:39:35.789675+00	2021-12-15 00:39:35.789898+00	f	\N	Assisted living	9	Middle School	hi	\N	Female-to-Male (FTM)/Transgender Male/Trans Man	Former smoker	Cigarette	\N	Half pack	2021-12-14	\N	2021-12-14	2-5 times/week	987	2021-12-30	2-5 times/week	Hepatitis	1-2 drinks/day	No	Occasional	9d36d544-2461-4abf-aaf6-188566879888	hj
91a6de6a-2607-4686-848c-5958e27267dc	2021-12-15 00:40:21.875269+00	2021-12-15 00:40:21.875319+00	f	\N	Assisted living	9	Middle School	hi	\N	Female-to-Male (FTM)/Transgender Male/Trans Man	Former smoker	Cigarette	\N	Half pack	2021-12-14	\N	2021-12-14	2-5 times/week	987	2021-12-30	Never	Hepatitis	1-2 drinks/day	Chewing tobacco	Occasional	9d36d544-2461-4abf-aaf6-188566879888	hj
36d67aa3-0864-4bab-b485-46137bffef69	2021-12-15 00:42:18.897613+00	2021-12-15 00:42:18.897652+00	f	\N	Apartment	9	Elementary school	TEST	\N	Male-to-Female (MTF)/Transgender Female/Trans Woman	Former smoker	Cigar	\N	Less than half pack	2021-12-14	\N	2021-12-14	0-1 times/week	987	2021-12-04	Always	Hepatitis	Occassionally	Chewing tobacco	Occasional	9d36d544-2461-4abf-aaf6-188566879888	TEST
3105b7f4-c6f4-4fd2-9f83-aeeb17dace43	2021-12-15 00:56:35.207266+00	2021-12-15 00:56:35.207328+00	f	\N	Assisted living	8	Middle School	Prodipta TESTING	Heterosexual (not lesbian, gay, or bisexual)	Female	Unknown if ever smoked	Chewing tobacco	\N	Less than 1 pack	2021-12-14	\N	2021-12-14	2-5 times/week	987	2021-12-10	Always	Asbestos	Occassionally	Cigarette	Occasional	9d36d544-2461-4abf-aaf6-188566879888	unmarried
5d4f61db-c34d-4292-8a93-c72f554be836	2021-12-17 07:57:44.619767+00	2021-12-17 07:57:44.619817+00	f	\N	Assisted living	9	Elementary school	TEST	Homosexual	Male-to-Female (MTF)/Transgender Female/Trans Woman	Former smoker	Cigar	\N	Less than 1 pack	2021-12-14	\N	2021-12-14	2-5 times/week	987	2021-12-10	Never	Hepatitis	Occassionally	Cigar	Never	9d36d544-2461-4abf-aaf6-188566879888	unmarried
a4513c36-6ad3-4fa4-8e6c-ec8eade4b169	2021-12-21 00:21:46.391665+00	2021-12-21 00:21:46.391729+00	f	\N	Apartment	7	Middle School	Prodipta TESTING	Homosexual	Male-to-Female (MTF)/Transgender Female/Trans Woman	Never smoker	Chewing tobacco	\N	Less than 1 pack	2021-12-14	\N	987	Never	987	2021-12-07	Always	Hepatitis	Occassionally	Chewing tobacco	Occasional	2e25724a-9018-499d-9250-eca8c7fd2a28	unmarried
\.


--
-- Data for Name: ehr_physicalexam; Type: TABLE DATA; Schema: public; Owner: sihan
--

COPY public.ehr_physicalexam (id, created_at, updated_at, is_deleted, deleted_at, general_appearance, head, eyes, ears, nose, throat, neck, cardiac, lungs, abdomen, musculoskeletal, back, extremities, lower_extremities, neurological, skin, res, psychiatric, rectal, patient_encounter_id) FROM stdin;
\.


--
-- Data for Name: ehr_planofcare; Type: TABLE DATA; Schema: public; Owner: sihan
--

COPY public.ehr_planofcare (id, created_at, updated_at, is_deleted, deleted_at, medical_notes, notes_html, patient_encounter_id) FROM stdin;
\.


--
-- Data for Name: ehr_reviewofsystem; Type: TABLE DATA; Schema: public; Owner: sihan
--

COPY public.ehr_reviewofsystem (id, created_at, updated_at, is_deleted, deleted_at, general, head, eyes, ears, nose, mouth, neck, breast, chest, heart, abdomen, gu, gyn, musculoskeletal, neurologic, psychiatric, patient_encounter_id) FROM stdin;
\.


--
-- Data for Name: ehr_vitals; Type: TABLE DATA; Schema: public; Owner: sihan
--

COPY public.ehr_vitals (id, created_at, updated_at, is_deleted, deleted_at, reading_date, reading_time, height, weight, bmi, temperature, pulse, respiratory_rate, o2_saturation, pain, blood_pressure, patient_encounter_id) FROM stdin;
e152ba4a-4b95-4f74-be57-321eed45a4ef	2021-12-23 02:29:27.021173+00	2021-12-23 02:29:27.021213+00	f	\N	2021-12-01	16:32:00	21	34	3554	23	1237345	2343	232	234	\N	2e25724a-9018-499d-9250-eca8c7fd2a28
c272f23c-95ed-4316-a4d0-9bfd0a62a901	2021-12-23 02:32:05.868395+00	2021-12-23 02:32:05.86843+00	f	\N	2021-12-08	17:31:00	23	123	123	10	23	234	234	234	\N	2e25724a-9018-499d-9250-eca8c7fd2a28
1fe307c9-8762-4efa-ada0-2db87341ba29	2021-12-23 02:45:35.309089+00	2021-12-23 02:45:35.309138+00	f	\N	2021-11-30	14:49:00	13	123	12312	12	123	126	12	1223	\N	2e25724a-9018-499d-9250-eca8c7fd2a28
13f8dc6b-b535-4832-9223-c643536b2995	2021-12-23 08:13:34.551484+00	2021-12-23 08:13:34.551525+00	f	\N	2021-12-23	20:12:00	156	370	22	56	67	454	65	4545	\N	7cb97c7b-b7c6-4f0e-b02b-93f5c0663006
e08ff325-88ed-4d3c-a53f-3150d76fc2db	2021-12-23 08:22:41.280829+00	2021-12-23 08:22:41.280872+00	f	\N	2021-12-23	20:12:00	156	370	22	56	67	454	656	4545	\N	7cb97c7b-b7c6-4f0e-b02b-93f5c0663006
f263adf4-e88e-479e-9152-5d33b9445d71	2021-12-23 13:06:44.728078+00	2021-12-23 13:06:44.728113+00	f	\N	2021-11-30	01:06:00	122	1212	12312	3123	12312	-21	123123	1313	\N	9d36d544-2461-4abf-aaf6-188566879888
b99e26c4-cd92-4a5e-a928-1e7963384cc2	2021-12-23 13:06:59.000547+00	2021-12-23 13:06:59.000581+00	f	\N	2021-11-30	01:06:00	122	1212	12312	3123	12312	-21	123123	13137	\N	9d36d544-2461-4abf-aaf6-188566879888
\.


--
-- Data for Name: inbox_inboxchannel; Type: TABLE DATA; Schema: public; Owner: sihan
--

COPY public.inbox_inboxchannel (id, created_at, updated_at, is_deleted, deleted_at, first_user_id, second_user_id) FROM stdin;
\.


--
-- Data for Name: inbox_inboxmessage; Type: TABLE DATA; Schema: public; Owner: sihan
--

COPY public.inbox_inboxmessage (id, created_at, updated_at, is_deleted, deleted_at, message, subject, read_status, channel_id, sender_id) FROM stdin;
\.


--
-- Data for Name: twilio_chat_waitingroom; Type: TABLE DATA; Schema: public; Owner: sihan
--

COPY public.twilio_chat_waitingroom (id, created_at, updated_at, is_deleted, deleted_at, text, room_media, doctor_id, room_media_mime_type) FROM stdin;
59b6bd5c-bcef-4e05-bce8-69fd40286199	2021-12-10 04:05:23.393729+00	2021-12-10 04:05:23.425081+00	f	\N	\N	doctor_waiting_room_media/1639130723.424511_file_example_MP4_480_1_5MG.mp4	0440043c-e650-410a-ab98-4fe6ba519ace	\N
5d23f12f-e50f-43c0-ab36-e8c4591bee10	2021-12-15 05:09:48.968127+00	2021-12-23 09:48:36.950149+00	f	\N	Welcome To this cool doctors room, Wait here		4fb7958b-94e4-4354-a641-3023a788ccc1	\N
58b649c8-9544-4e3c-b45b-48832ecc3298	2021-12-17 16:10:31.263477+00	2021-12-17 16:49:42.17991+00	f	\N	Hello Patients. Please make yourself comfortable. I'll be right with you soon	doctor_waiting_room_media/KlikPharmacyTest.jpg	384b0671-0a92-435b-b289-6d59686517b6	image/jpeg
\.


--
-- Data for Name: user_clinicinfo; Type: TABLE DATA; Schema: public; Owner: sihan
--

COPY public.user_clinicinfo (id, created_at, updated_at, is_deleted, deleted_at, username, number_of_practitioners, user_id, notification_email, website, _license_file, license_expiration) FROM stdin;
f5dbecdf-b09f-4081-adee-313919b184fd	2021-11-27 08:26:59.403016+00	2021-11-27 08:26:59.403062+00	f	\N	prodipta.banerjee	0	77ffd331-ced9-46e1-947c-d445565eecce	\N	\N	\N	\N
a544565a-3a1e-4777-95b8-f4125cf32002	2021-11-28 08:15:39.200628+00	2021-11-28 08:15:39.200681+00	f	\N	pro.1	88	c5ce351d-b516-4a27-b62a-30eb1ec98025	\N	\N	\N	\N
cadae86f-9f72-4577-a7d9-c22fc5d0661d	2021-11-29 05:26:53.77461+00	2021-11-29 05:26:53.774659+00	f	\N	random	10	17e97df5-162c-45ec-a190-79626b980f4b	\N	\N	\N	\N
9a37a610-4e51-43f5-aa26-ba24e4d7095c	2021-11-29 08:27:24.686765+00	2021-11-29 08:27:24.686827+00	f	\N	st.marys.hospital	4	f0eb657a-57e3-4d10-b336-8523c5a02050	\N	\N	\N	\N
2fc8be03-a9cd-4883-9b0d-2cc6353d65ff	2021-11-30 05:37:57.637601+00	2021-11-30 05:37:57.637647+00	f	\N	l.hospital	2	633420fb-e20c-4deb-8162-bedcd3d92c68	\N	\N	\N	\N
5e902938-6539-4e45-bbb8-3e2f335167e5	2021-11-30 05:39:51.151903+00	2021-11-30 05:39:51.151948+00	f	\N	l.hospital.1	2	c739b88f-ffa9-4e03-9a5f-f9064b472b65	\N	\N	\N	\N
ed2d2dab-439d-485a-95c8-c97cacc63b9a	2021-11-30 05:43:57.615574+00	2021-11-30 05:43:57.615624+00	f	\N	new.hospital	2	c1f9bc20-8e97-4e7a-b2a1-2419ede06191	\N	\N	\N	\N
1206ed70-e74b-4aee-83e4-ca732c6d2574	2021-11-30 05:46:32.805067+00	2021-11-30 05:46:32.805179+00	f	\N	jason’s.hospital	2	bddf4b1e-3a5b-4f13-a89f-c43b79d9cfde	\N	\N	\N	\N
be0e2501-413b-4089-8283-7936c53679d2	2021-11-30 05:49:09.495061+00	2021-11-30 05:49:09.495108+00	f	\N	hospital	2	245b2b72-4fae-40ac-bab1-f3cfc0f70c42	\N	\N	\N	\N
a062d595-13a2-4fba-be43-49a591644769	2021-11-30 05:53:33.219001+00	2021-11-30 05:53:33.219053+00	f	\N	hospital.1	2	91d1b59d-b202-486a-bfcc-d9c0490a88f7	\N	\N	\N	\N
17cd5a29-6517-4c53-8c8f-d4419b14f296	2021-11-30 06:33:34.720968+00	2021-11-30 06:33:34.721005+00	f	\N	hospital.2	2	dd7346c1-32db-48dd-8274-c4eca960836c	\N	\N	\N	\N
08111764-811e-4ea6-a307-8df31282aea5	2021-11-30 06:45:08.458155+00	2021-11-30 06:45:08.458277+00	f	\N	hehe.hospital	3	88efdf2d-bec2-4221-9196-a11ef2391bd3	\N	\N	\N	\N
1abcaa96-8c3c-4ba4-9a43-41fc9f8acc05	2021-11-30 06:47:33.364173+00	2021-11-30 06:47:33.364234+00	f	\N	hehe.hospital.1	3	a2d0ca75-c7b0-4ccd-bdcb-9fcfd76db504	\N	\N	\N	\N
c13d9cd7-12e7-4d17-9437-1672abb137bc	2021-11-30 06:50:52.728302+00	2021-11-30 06:50:52.728357+00	f	\N	hospital.keys.khulsi	2	cbff03a1-de8f-4f06-be55-6689d56b5c91	\N	\N	\N	\N
3552e53e-137c-4ffd-bf92-7d1b8c802c51	2021-11-30 06:53:36.564539+00	2021-11-30 06:53:36.564646+00	f	\N	hospital.keys.noting	3	8c268125-2199-4272-ad77-6e857678702a	\N	\N	\N	\N
be99ded9-7fd9-48bd-83e3-4e132d01f6ca	2021-11-30 06:57:04.49352+00	2021-11-30 06:57:04.493574+00	f	\N	jason.baha’i.we	24	75a74960-1352-4fc4-97a8-eba612426c7c	\N	\N	\N	\N
25972787-38fd-4f5a-87bc-d61a2c20a590	2021-11-30 08:02:13.281411+00	2021-11-30 08:02:13.28147+00	f	\N	lama.hospital	34	4ebfc00b-4b4a-442a-b135-782bcc6b112e	\N	\N	\N	\N
36aa1141-2b1f-462d-8b91-9db06d33f1c0	2021-11-30 08:05:25.55494+00	2021-11-30 08:05:25.554992+00	f	\N	hehe.hospital.2	56	35c8c822-025c-4342-8fb0-424af92b2cc8	\N	\N	\N	\N
aee477bf-c3ac-4b18-b0e0-0fdef47b3ffe	2021-12-03 06:15:45.923193+00	2021-12-03 06:15:45.923258+00	f	\N	hospital.5	2	977bbe34-1fd2-435b-b1f5-bf90d363f34f	\N	\N	\N	\N
7d90aad1-ef5d-46db-90b8-d001b2133f91	2021-12-03 06:23:31.151629+00	2021-12-03 06:23:31.151739+00	f	\N	hospital.name	3	1dc9b5f7-ef76-4c5f-9986-27f8eb721295	\N	\N	\N	\N
032d0067-ff67-432c-b9ee-0b969d8a41d7	2021-12-03 06:28:03.474317+00	2021-12-03 06:28:03.474377+00	f	\N	hospital.name.1	3	7d634e50-e284-4ecd-a54d-889bd138223c	\N	\N	\N	\N
4746121b-1b03-4abe-9ffc-c4dbb26736e8	2021-12-03 06:30:21.292811+00	2021-12-03 06:30:21.292869+00	f	\N	hospital.8	9	27911350-88bb-43ff-85c6-d0347936563e	\N	\N	\N	\N
ad2ce6b3-ce95-4905-b8e0-3ae84f60a606	2021-12-03 07:06:31.920966+00	2021-12-03 07:06:31.921012+00	f	\N	hospital.9	56	a91af88c-fc35-46b5-8831-5e23c00abbbc	\N	\N	\N	\N
9069f1cd-dfa7-4155-b38e-562b7bf242d0	2021-12-03 10:38:30.876295+00	2021-12-03 10:38:30.876373+00	f	\N	new.clinic	5	b8c2953f-2b6b-4407-a54c-7416f78541e9	\N	\N	\N	\N
db405f0b-f643-4657-bd0a-68703626efaa	2021-12-03 13:50:06.404734+00	2021-12-03 13:50:06.404802+00	f	\N	klik.hospital	6	f7eb6b06-45b4-4b44-afd0-2544d3284303	\N	\N	\N	\N
f77a7faa-4c3e-4f03-8f8b-d9bab5495c3f	2021-12-08 05:30:56.996005+00	2021-12-08 05:30:56.996056+00	f	\N	clinic.name	5	3beb642d-d876-4d39-8539-8efb9def2622	\N	\N	\N	\N
280befa4-92a3-4e41-9c2b-363d816da1de	2021-12-10 15:34:27.698609+00	2021-12-10 15:34:27.698652+00	f	\N	dokto-hospital	4	bddc3d89-087a-4ff0-9101-58ff4633bf74	\N	\N	\N	\N
65affdbd-0d43-4f71-bff1-b61d63b0d3f3	2021-12-14 17:02:15.112112+00	2021-12-23 13:17:07.972597+00	f	\N	hospital-name	26	70b8af3e-d59d-48e7-90e6-ded64489cf7f	\N	https://www.google.com		2021-12-24
89c98c9c-1e06-4e21-90e1-300c4241e532	2021-12-15 07:24:54.295642+00	2021-12-15 07:24:54.295718+00	f	\N	sihan-tawsik	1	2c32724e-8565-4a35-84d7-430b411c83be	\N	\N	\N	\N
efbf0788-29aa-4420-9088-73042f006b0c	2021-12-20 08:26:14.884457+00	2021-12-20 08:26:14.884499+00	f	\N	meh	12	e7556c15-90eb-42ab-b45c-0ab6cf333068	\N	\N	\N	\N
a1515975-4821-466a-8071-628c28faf0ec	2021-12-20 22:30:41.043544+00	2021-12-20 22:30:41.043595+00	f	\N	abdul-hospital-and-co	1	881eb97b-ce35-4df5-8aaf-0c688c34f00c	\N	\N	\N	\N
\.


--
-- Data for Name: user_doctoracceptedinsurance; Type: TABLE DATA; Schema: public; Owner: sihan
--

COPY public.user_doctoracceptedinsurance (id, created_at, updated_at, is_deleted, deleted_at, insurance, doctor_info_id) FROM stdin;
eebb4801-b759-4a57-ab6f-39ef412b1b0a	2021-12-17 06:54:47.731096+00	2021-12-17 06:54:47.731133+00	f	\N	all	fc68f79b-79db-439d-958c-b5d8eed2ce02
15d271f4-3450-4fef-93da-3dd135a05adc	2021-12-20 09:03:50.044007+00	2021-12-20 09:03:50.044074+00	f	\N	Alabama	4fb7958b-94e4-4354-a641-3023a788ccc1
5e97c361-9da4-4457-99f7-ab5f0f693cc8	2021-12-21 10:46:04.559064+00	2021-12-21 10:46:04.559113+00	f	\N	Blue Cross and Blue Shield Association	4fb7958b-94e4-4354-a641-3023a788ccc1
4e34a986-24ff-497d-bd3a-b9255bd8b096	2021-12-21 10:46:04.55915+00	2021-12-21 10:46:04.55916+00	f	\N	Horace Mann Educators Corporation	4fb7958b-94e4-4354-a641-3023a788ccc1
9c06513b-a508-4d65-b283-eb0cb755bba9	2021-12-21 10:46:04.55918+00	2021-12-21 10:46:04.559188+00	f	\N	Blue Cross Blue Shield of Tennessee	4fb7958b-94e4-4354-a641-3023a788ccc1
2de9fa1b-7757-4d84-999f-7ad0d1d3885c	2021-12-21 10:46:04.559205+00	2021-12-21 10:46:04.559213+00	f	\N	Independence Health Group	4fb7958b-94e4-4354-a641-3023a788ccc1
f50f4bd7-79c4-406e-80e9-12fc7aed173c	2021-12-21 10:46:04.55923+00	2021-12-21 10:46:04.559238+00	f	\N	MassHealth	4fb7958b-94e4-4354-a641-3023a788ccc1
5ee25e11-8e40-4843-b4a5-2cb37e46620d	2021-12-21 10:46:04.559256+00	2021-12-21 10:46:04.559267+00	f	\N	Highmark	4fb7958b-94e4-4354-a641-3023a788ccc1
220b0658-99ae-4887-9bf1-a085f2ff7065	2021-12-22 08:27:02.426996+00	2021-12-22 08:27:02.42704+00	f	\N	AARP	067f05d0-8a29-4c5c-b070-faa7a0ac9ddc
62894145-1a99-47e7-8650-f09a8fb8b3e2	2021-12-22 08:27:02.427075+00	2021-12-22 08:27:02.427085+00	f	\N	Alabama	067f05d0-8a29-4c5c-b070-faa7a0ac9ddc
0f0b8115-08c3-4e8f-8879-3d70280fa2d7	2021-12-22 10:18:15.321226+00	2021-12-22 10:18:15.32128+00	f	\N	all	8504ee48-62f2-4f2c-bbb1-b57f65b9f92d
65b65e7d-6bb3-4d86-8074-6eb503ca2d21	2021-12-24 05:15:38.566046+00	2021-12-24 05:15:38.566084+00	f	\N	Alabama	135f16d8-b14c-40cb-a333-787296d86890
0d256833-61c3-4858-a56e-0e52a32d8545	2021-12-24 05:15:38.566129+00	2021-12-24 05:15:38.566138+00	f	\N	American Family Insurance	135f16d8-b14c-40cb-a333-787296d86890
\.


--
-- Data for Name: user_doctoravailablehours; Type: TABLE DATA; Schema: public; Owner: sihan
--

COPY public.user_doctoravailablehours (id, created_at, updated_at, is_deleted, deleted_at, day_of_week, start_time, end_time, doctor_info_id) FROM stdin;
\.


--
-- Data for Name: user_doctoreducation; Type: TABLE DATA; Schema: public; Owner: sihan
--

COPY public.user_doctoreducation (id, created_at, updated_at, is_deleted, deleted_at, course, year, college, doctor_info_id) FROM stdin;
b1e744ca-2068-4516-8431-f364186ad47c	2021-11-27 07:06:03.460285+00	2021-11-27 07:06:03.460351+00	f	\N	Onek porsi	2021-11-26	Pori nai	a354ca46-0d86-4f96-8cdb-590a8986513b
b5cf3ddd-1204-4043-b999-42f46b9ff546	2021-11-27 07:07:10.443964+00	2021-11-27 07:07:10.444027+00	f	\N	ab	2021-11-08	ab college	90714f3d-d654-4c8e-b15d-2a08d819f96c
6ea230b7-87cb-4d31-a754-eede602c614f	2021-11-30 11:43:25.036538+00	2021-11-30 11:43:25.036572+00	f	\N	test course	2021-11-29	test college	46794c6f-add0-496e-83a5-516b922623d0
6e59e4e2-7684-44b6-b2c2-9c7a55d0ce38	2021-12-01 00:20:44.596156+00	2021-12-01 00:20:44.596297+00	f	\N	test course	2021-11-29	test college	1412adfb-1919-4c80-905b-e0e4cb60d8c0
47b5b97b-9b20-4fba-b1a5-3793f5770489	2021-12-03 06:14:04.590067+00	2021-12-03 06:14:04.590121+00	f	\N	test course	2021-11-29	test college	236650ea-d8e1-4b34-b0c6-ddf3d21908c9
d04cc870-bee7-4e29-af05-1b4cecd97fa3	2021-12-03 10:37:13.334523+00	2021-12-03 10:37:13.334576+00	f	\N	ourses	2021-12-03	new college	fff581d1-3363-43b5-99ae-41830c49a56d
9080572f-1952-4ddb-99bf-ee5f0fd0a80a	2021-12-03 10:37:13.341721+00	2021-12-03 10:37:13.341764+00	f	\N	test course	2021-11-29	test college	fff581d1-3363-43b5-99ae-41830c49a56d
76af0381-4eeb-4ae1-b070-60165989ea30	2021-12-04 17:42:50.39113+00	2021-12-04 17:42:50.391164+00	f	\N	test course	2021-12-04	test college	afc72cb3-f523-41f0-9934-998199deb882
1879fda4-f857-4e2e-8074-81e3656e852d	2021-12-07 12:52:54.158994+00	2021-12-07 12:52:54.159031+00	f	\N	string	string	string	39b6fb65-d885-40c7-a8c5-e52904ba264a
aff9b4ee-b486-4537-ab8a-72056440e912	2021-12-07 13:37:31.44358+00	2021-12-07 13:37:31.443648+00	f	\N	string	2022-12-01	string	0440043c-e650-410a-ab98-4fe6ba519ace
51395d53-f3e0-4939-828e-be0a6682b407	2021-12-07 13:37:47.224926+00	2021-12-07 13:37:47.224983+00	f	\N	string	2022-12-01	string	0440043c-e650-410a-ab98-4fe6ba519ace
a3be69a0-79d0-44b5-b122-290cf56e208e	2021-12-08 04:49:00.752897+00	2021-12-08 04:49:00.752948+00	f	\N	yet another course	2021-12-08	yet another college	1433ed23-9b64-43ad-a0d7-2d1ed6882a4e
acfa6954-24e3-46c1-a376-128ae33f284e	2021-12-09 13:15:21.109327+00	2021-12-09 13:15:21.109367+00	f	\N	Medicine	2005-01-01	U of A	384b0671-0a92-435b-b289-6d59686517b6
ab000210-d069-4f6d-89ab-163d7ea3200c	2021-12-10 04:42:41.550639+00	2021-12-10 04:42:41.550686+00	f	\N	asdasd	2021-12-01	sadasd	4ef8a711-620e-49cb-85c8-12b6594e7b07
97a0ee60-7a62-4f91-ba01-ffd3ea9a583f	2021-12-17 06:54:47.724844+00	2021-12-17 06:54:47.724878+00	f	\N	abc	2021-12-08	ab college	fc68f79b-79db-439d-958c-b5d8eed2ce02
9d382cf7-1f49-425a-8f91-69f845bf783e	2021-12-22 08:27:02.414745+00	2021-12-22 08:27:02.414782+00	f	\N	notre	2021-12-21	notre	067f05d0-8a29-4c5c-b070-faa7a0ac9ddc
e483ac62-5733-42d9-bfd5-8203d78c1a12	2021-12-22 10:18:15.314619+00	2021-12-22 10:18:15.314661+00	f	\N	hhdhd	2021-12-18	bdgdgd	8504ee48-62f2-4f2c-bbb1-b57f65b9f92d
6f3c816e-8f79-4907-9e18-e1479cbbf2ef	2021-12-22 11:40:48.540397+00	2021-12-22 11:40:48.540442+00	f	\N	MD, FCCP	2012-11-01	University of Southern California	4fb7958b-94e4-4354-a641-3023a788ccc1
fc00d7e3-4933-4672-9d66-763de496bc68	2021-12-22 11:40:48.547526+00	2021-12-22 11:40:48.547593+00	f	\N	yet another course	2021-12-22	yet another college	4fb7958b-94e4-4354-a641-3023a788ccc1
ecb76395-3814-446f-b755-1ebe257f5833	2021-12-24 05:15:38.555301+00	2021-12-24 05:15:38.555336+00	f	\N	Hello	2021-12-24	Hey	135f16d8-b14c-40cb-a333-787296d86890
\.


--
-- Data for Name: user_doctorexperience; Type: TABLE DATA; Schema: public; Owner: sihan
--

COPY public.user_doctorexperience (id, created_at, updated_at, is_deleted, deleted_at, establishment_name, job_title, start_date, end_date, job_description, doctor_info_id) FROM stdin;
65b144eb-0a95-474b-8de8-6b98ce049eb3	2021-11-27 07:06:03.509872+00	2021-11-27 07:06:03.509939+00	f	\N	korsi kaaj	Doc Oc	2021-11-25	2021-11-27	hehe	a354ca46-0d86-4f96-8cdb-590a8986513b
b129d228-281f-49e6-bc6c-8b7bfc8017a8	2021-11-27 07:07:10.480026+00	2021-11-27 07:07:10.480184+00	f	\N	ab	abcd	2021-11-11	2021-11-25	abcd	90714f3d-d654-4c8e-b15d-2a08d819f96c
33d8f524-bbb5-458c-98a3-bceb8bed163e	2021-11-27 07:11:48.400566+00	2021-11-27 07:11:48.400607+00	f	\N	abc	abcde	2021-11-11	2021-11-25	abcd	0440043c-e650-410a-ab98-4fe6ba519ace
f4e05a9e-0f60-46a1-a6ad-3e57243147c2	2021-11-30 11:43:25.041608+00	2021-11-30 11:43:25.041647+00	f	\N	test establishment	test title	2021-11-29	\N	\N	46794c6f-add0-496e-83a5-516b922623d0
69c6278d-1c35-4bef-9dd0-ee9b896de029	2021-12-01 00:20:44.617804+00	2021-12-01 00:20:44.617879+00	f	\N	test establishment	test title	2021-11-29	\N	\N	1412adfb-1919-4c80-905b-e0e4cb60d8c0
cd25d150-cf1f-4107-b30d-cb9b80f80882	2021-12-03 06:14:04.601003+00	2021-12-03 06:14:04.601064+00	f	\N	test establishment	test title	2012-03-03	2020-04-03	\N	236650ea-d8e1-4b34-b0c6-ddf3d21908c9
47520bcf-a377-4c95-8a6f-2d30322d6d97	2021-12-03 10:37:13.34849+00	2021-12-03 10:37:13.348548+00	f	\N	test establishment	test title	2021-11-29	\N	\N	fff581d1-3363-43b5-99ae-41830c49a56d
8c0dc20d-f992-47bc-93fe-0ebd66df9641	2021-12-04 17:42:50.395895+00	2021-12-04 17:42:50.395934+00	f	\N	clinic test	doctor	2021-12-04	\N	test description	afc72cb3-f523-41f0-9934-998199deb882
d736839d-190f-4178-8d39-99a1bf743769	2021-12-07 12:52:54.165034+00	2021-12-07 12:52:54.165072+00	f	\N	string	string	2021-11-18	2021-11-18	string	39b6fb65-d885-40c7-a8c5-e52904ba264a
1e3bd713-d981-44fb-aae4-33732b784e2d	2021-12-07 13:18:45.016325+00	2021-12-07 13:19:33.347846+00	f	\N	Mayo Clinic	Director	2021-12-01	2021-12-07	Directed as the head of pulmonary department.	4fb7958b-94e4-4354-a641-3023a788ccc1
d3c96664-8129-4915-8024-2455fd1b5978	2021-12-08 04:49:00.759226+00	2021-12-08 04:49:00.759268+00	f	\N	test establishment	Fancy Job Title	2021-01-05	2021-12-08	jkahfjksdkjfjksdf	1433ed23-9b64-43ad-a0d7-2d1ed6882a4e
02830bed-a48a-4f34-a477-b3ee9fa6b4e5	2021-12-10 04:42:41.558706+00	2021-12-10 04:42:41.558757+00	f	\N	sdad	asdasd	2021-12-02	2021-12-10	sdasdas	4ef8a711-620e-49cb-85c8-12b6594e7b07
98086707-20a5-4213-823c-77cd1a14923c	2021-12-22 08:27:02.419952+00	2021-12-22 08:27:02.420001+00	f	\N	ayhay	hehe	2021-12-16	2021-12-22	hehe	067f05d0-8a29-4c5c-b070-faa7a0ac9ddc
1d10f09a-09af-4219-93fe-d811355a93ae	2021-12-24 05:15:38.56043+00	2021-12-24 05:15:38.560466+00	f	\N	Hello	No	2021-12-06	2021-12-24	Hello	135f16d8-b14c-40cb-a333-787296d86890
\.


--
-- Data for Name: user_doctorinfo; Type: TABLE DATA; Schema: public; Owner: sihan
--

COPY public.user_doctorinfo (id, created_at, updated_at, is_deleted, deleted_at, username, date_of_birth, country, gender, identification_type, identification_number, _identification_photo, professional_bio, linkedin_url, facebook_url, twitter_url, awards, _license_file, notification_email, reason_to_delete, temporary_disable, accepted_insurance, user_id, profession, license_expiration) FROM stdin;
a354ca46-0d86-4f96-8cdb-590a8986513b	2021-11-27 07:06:03.333513+00	2021-12-20 13:03:03.901918+00	f	\N	sanviraj.zahin.haque	1998-08-12	Bangladesh	MALE	DRIVER'S LICENSE	111111111	doctor_identification_photo/a354ca46-0d86-4f96-8cdb-590a8986513b_2021_11_27_13_06_03_349700.jpeg	hehe , onek bio	\N	\N	\N	hehe	doctor_license_file/a354ca46-0d86-4f96-8cdb-590a8986513b_2021_11_27_13_06_03_388175.jpeg	sihantawsik@gmail.com	\N	t	\N	09a95982-a373-4555-9347-b963628701ac	\N	\N
90714f3d-d654-4c8e-b15d-2a08d819f96c	2021-11-27 07:07:10.30682+00	2021-12-04 12:57:44.660977+00	f	\N	dr.s.ahmed	2021-11-08	Bangladesh	MALE	PASSPORT	1234	doctor_identification_photo/90714f3d-d654-4c8e-b15d-2a08d819f96c_2021_11_27_13_07_10_324652.webp	abcd	\N	\N	\N	\N	doctor_license_file/90714f3d-d654-4c8e-b15d-2a08d819f96c_2021_11_27_13_07_10_379443.webp	\N	\N	f	\N	1dd1ffe0-2113-4c97-bcf2-abe2798bba3d	\N	\N
4fb7958b-94e4-4354-a641-3023a788ccc1	2021-11-27 07:11:07.991893+00	2021-12-22 06:30:01.734729+00	t	\N	mahmudul	2021-11-08	Bangladesh	MALE	PASSPORT	1234	doctor_identification_photo/4fb7958b-94e4-4354-a641-3023a788ccc1_2021_11_27_13_11_08_001262.webp	Mahmudul Alam, MD, FCCP, is a graduate of George Washington University Medical School.	\N	\N	\N			testingdoktohehe@gmail.com	NOT SATISFIED WITH THE SERVICE	f	\N	952478f7-4c6e-497a-b6c0-7f11ca93ae12	\N	2021-12-30
0440043c-e650-410a-ab98-4fe6ba519ace	2021-11-27 07:11:48.31574+00	2021-12-20 12:57:35.315769+00	f	\N	sihan	2021-11-08	Bangladesh	MALE	PASSPORT	1234	doctor_identification_photo/0440043c-e650-410a-ab98-4fe6ba519ace_2021_11_27_13_11_48_325837.webp	abcd	\N	\N	\N	\N	doctor_license_file/0440043c-e650-410a-ab98-4fe6ba519ace_2021_11_27_13_11_48_350262.webp	\N	\N	f	\N	3a0edd9f-747f-4c4d-b271-bc6b38696fe4	\N	\N
46794c6f-add0-496e-83a5-516b922623d0	2021-11-30 11:43:25.010909+00	2021-11-30 11:43:25.030384+00	f	\N	full.name	2021-11-30	Bangladesh	MALE	PASSPORT	3479738523872	doctor_identification_photo/46794c6f-add0-496e-83a5-516b922623d0_2021_11_30_17_43_25_017487.jpeg	Test bio	\N	\N	\N	\N	doctor_license_file/46794c6f-add0-496e-83a5-516b922623d0_2021_11_30_17_43_25_026214.jpeg	\N	\N	f	\N	a81869fe-3d7e-4a82-b9a7-239311c5c5a2	\N	\N
1412adfb-1919-4c80-905b-e0e4cb60d8c0	2021-12-01 00:20:44.546682+00	2021-12-01 00:20:44.587737+00	f	\N	full.name.1	2021-12-01	Bangladesh	MALE	PASSPORT	3479738523872	doctor_identification_photo/1412adfb-1919-4c80-905b-e0e4cb60d8c0_2021_12_01_06_20_44_568246.jpeg	Test bio	\N	\N	\N	\N	doctor_license_file/1412adfb-1919-4c80-905b-e0e4cb60d8c0_2021_12_01_06_20_44_579041.jpeg	\N	\N	f	\N	969142a9-3a26-45f1-952e-6ec5d0e6fa1a	\N	\N
236650ea-d8e1-4b34-b0c6-ddf3d21908c9	2021-12-03 06:14:04.553844+00	2021-12-03 06:14:04.581763+00	f	\N	mr..john.doe	2000-09-27	Bangladesh	MALE	STATE ID	139494948	doctor_identification_photo/236650ea-d8e1-4b34-b0c6-ddf3d21908c9_2021_12_03_12_14_04_561520.jpeg	Test bio	\N	\N	\N	\N	doctor_license_file/236650ea-d8e1-4b34-b0c6-ddf3d21908c9_2021_12_03_12_14_04_575313.jpeg	\N	\N	f	\N	ed504b9b-7ed0-403a-b26b-003cbbad9b36	\N	\N
fff581d1-3363-43b5-99ae-41830c49a56d	2021-12-03 10:37:13.307078+00	2021-12-03 10:37:13.326341+00	f	\N	full.name.2	1994-12-26	Bangladesh	MALE	STATE ID	3479738523872	doctor_identification_photo/fff581d1-3363-43b5-99ae-41830c49a56d_2021_12_03_16_37_13_310811.jpeg	Test bio	\N	\N	\N	\N	doctor_license_file/fff581d1-3363-43b5-99ae-41830c49a56d_2021_12_03_16_37_13_319977.jpeg	\N	\N	f	\N	81a1c762-0527-457c-88f4-ac0dd02e870d	\N	\N
afc72cb3-f523-41f0-9934-998199deb882	2021-12-04 17:42:50.371312+00	2021-12-04 17:42:50.386129+00	f	\N	shafayat.hossain	2021-12-04	Angola	MALE	PASSPORT	12345670	doctor_identification_photo/afc72cb3-f523-41f0-9934-998199deb882_2021_12_04_23_42_50_374533.png	This is a test bio	\N	\N	\N	\N	doctor_license_file/afc72cb3-f523-41f0-9934-998199deb882_2021_12_04_23_42_50_382066.jpeg	\N	\N	f	\N	5faf1dc6-fa78-4082-b4a6-8b2a00cd715d	\N	\N
39b6fb65-d885-40c7-a8c5-e52904ba264a	2021-12-07 12:52:54.112686+00	2021-12-07 12:52:54.152967+00	f	\N	mahmudul.alam	2021-11-18	string	MALE	PASSPORT	string	doctor_identification_photo/39b6fb65-d885-40c7-a8c5-e52904ba264a_2021_12_07_18_52_54_115412.jpeg	string	\N	\N	\N	string	doctor_license_file/39b6fb65-d885-40c7-a8c5-e52904ba264a_2021_12_07_18_52_54_134713.jpeg	\N	\N	f	\N	64f65ba5-7d1d-4bfb-a54a-cb94b271e652	\N	\N
1433ed23-9b64-43ad-a0d7-2d1ed6882a4e	2021-12-08 04:49:00.72797+00	2021-12-08 04:49:00.746166+00	f	\N	samnan.rahee	2021-12-08	United Kingdom	MALE	DRIVER'S LICENSE	test_122344	doctor_identification_photo/1433ed23-9b64-43ad-a0d7-2d1ed6882a4e_2021_12_08_10_49_00_731370.png	test bio	\N	\N	\N	Publications	doctor_license_file/1433ed23-9b64-43ad-a0d7-2d1ed6882a4e_2021_12_08_10_49_00_740130.png	\N	\N	f	\N	89a45785-8ce9-4605-b28a-e123a7c47025	\N	\N
384b0671-0a92-435b-b289-6d59686517b6	2021-12-09 13:15:21.083999+00	2021-12-09 13:15:21.102991+00	f	\N	david-test	1944-01-01	United States	MALE	DRIVER'S LICENSE	D89765	doctor_identification_photo/384b0671-0a92-435b-b289-6d59686517b6_2021_12_09_19_15_21_087823.png	Excellent Doctor	\N	\N	\N	\N	doctor_license_file/384b0671-0a92-435b-b289-6d59686517b6_2021_12_09_19_15_21_097055.png	\N	\N	f	\N	fbfe7a13-6ef7-4094-b211-6407aeeb1f30	\N	\N
4ef8a711-620e-49cb-85c8-12b6594e7b07	2021-12-10 04:42:41.514317+00	2021-12-10 04:42:41.538464+00	f	\N	sihan-tawsik	1999-01-18	Bangladesh	MALE	PASSPORT	1234asd	doctor_identification_photo/4ef8a711-620e-49cb-85c8-12b6594e7b07_2021_12_10_10_42_41_518516.jpeg	sadasda	\N	\N	\N	asdasda	doctor_license_file/4ef8a711-620e-49cb-85c8-12b6594e7b07_2021_12_10_10_42_41_532117.jpeg	\N	\N	f	\N	fc8297cd-9b86-4033-a97e-da5abe71d76f	\N	\N
fc68f79b-79db-439d-958c-b5d8eed2ce02	2021-12-17 06:54:47.705497+00	2021-12-17 06:54:47.719249+00	f	\N	sihan-tawsik-1	2003-12-10	Bangladesh	MALE	PASSPORT	eddqd	doctor_identification_photo/fc68f79b-79db-439d-958c-b5d8eed2ce02_2021_12_17_12_54_47_707632.jpeg	sdas	\N	\N	\N	asdasd	doctor_license_file/fc68f79b-79db-439d-958c-b5d8eed2ce02_2021_12_17_12_54_47_714859.jpeg	\N	\N	f	\N	03f1a586-fb3e-4480-8d04-9273bb383245	\N	2021-12-21
067f05d0-8a29-4c5c-b070-faa7a0ac9ddc	2021-12-22 08:27:02.391428+00	2021-12-22 08:27:02.408515+00	f	\N	sanviraj-zahin-haque	2003-12-18	Bangladesh	MALE	PASSPORT	1111111111	doctor_identification_photo/067f05d0-8a29-4c5c-b070-faa7a0ac9ddc_2021_12_22_14_27_02_394124.png	aww	\N	\N	\N	ok	doctor_license_file/067f05d0-8a29-4c5c-b070-faa7a0ac9ddc_2021_12_22_14_27_02_403966.png	\N	\N	f	\N	0f219fd8-c6b7-4823-a783-b0900d6743ab	\N	2022-01-07
8504ee48-62f2-4f2c-bbb1-b57f65b9f92d	2021-12-22 10:18:15.28297+00	2021-12-22 10:18:15.308559+00	f	\N	oyetayo-tosin-tunde	2003-12-22	Nigeria	MALE	DRIVER'S LICENSE	73883939393	doctor_identification_photo/8504ee48-62f2-4f2c-bbb1-b57f65b9f92d_2021_12_22_16_18_15_285577.png	dhhdhd	\N	\N	\N	\N	doctor_license_file/8504ee48-62f2-4f2c-bbb1-b57f65b9f92d_2021_12_22_16_18_15_301593.jpeg	\N	\N	f	\N	8bf64794-80d0-4d64-bfc3-8a167f4f8960	\N	2022-02-26
135f16d8-b14c-40cb-a333-787296d86890	2021-12-24 05:15:38.480671+00	2021-12-24 05:15:38.549003+00	f	\N	sanviraj-zahin-haque-1	2003-12-09	Bangladesh	MALE	PASSPORT	111111	doctor_identification_photo/135f16d8-b14c-40cb-a333-787296d86890_2021_12_24_11_15_38_483260.jpeg	Hello	\N	\N	\N	\N	doctor_license_file/135f16d8-b14c-40cb-a333-787296d86890_2021_12_24_11_15_38_497075.jpeg	\N	\N	f	\N	444d8a39-22e2-4544-a261-0ec6fc70215c	\N	2021-12-31
\.


--
-- Data for Name: user_doctorlanguage; Type: TABLE DATA; Schema: public; Owner: sihan
--

COPY public.user_doctorlanguage (id, created_at, updated_at, is_deleted, deleted_at, language, doctor_info_id) FROM stdin;
93627902-6a82-4d44-89cc-fc9b3dbd3136	2021-11-27 07:06:03.604802+00	2021-11-27 07:06:03.604876+00	f	\N	Spanish	a354ca46-0d86-4f96-8cdb-590a8986513b
a9347fce-4311-4232-b1b6-230b6c66a603	2021-11-27 07:06:03.604952+00	2021-11-27 07:06:03.604972+00	f	\N	English	a354ca46-0d86-4f96-8cdb-590a8986513b
ca3cf7d8-630c-491d-8720-424add7c9558	2021-11-27 07:07:10.535015+00	2021-11-27 07:07:10.53509+00	f	\N	English	90714f3d-d654-4c8e-b15d-2a08d819f96c
9ee3d3dc-ed85-4fac-aadd-bd462a9c1957	2021-11-27 07:11:08.099179+00	2021-11-27 07:11:08.099222+00	f	\N	English	4fb7958b-94e4-4354-a641-3023a788ccc1
c4646c9a-c827-4052-a16f-886d5695960b	2021-11-27 07:11:48.437873+00	2021-11-27 07:11:48.437933+00	f	\N	English	0440043c-e650-410a-ab98-4fe6ba519ace
e7c49018-6c1e-41af-85ab-2ac21587f8b0	2021-11-30 11:43:25.051647+00	2021-11-30 11:43:25.051753+00	f	\N	English	46794c6f-add0-496e-83a5-516b922623d0
ec58ed9e-4f59-4cf2-a1b9-7bf3c8b8d31e	2021-11-30 11:43:25.051806+00	2021-11-30 11:43:25.051815+00	f	\N	Spanish	46794c6f-add0-496e-83a5-516b922623d0
4186bd20-71ad-4e6c-a9b5-75f74dfad12f	2021-11-30 11:43:25.051834+00	2021-11-30 11:43:25.051842+00	f	\N	French	46794c6f-add0-496e-83a5-516b922623d0
b32225f5-898e-43c2-8423-2f042388d9cc	2021-12-01 00:20:44.637631+00	2021-12-01 00:20:44.637689+00	f	\N	English	1412adfb-1919-4c80-905b-e0e4cb60d8c0
241add70-ef15-45f5-a6da-4ed7d24e1692	2021-12-01 00:20:44.637746+00	2021-12-01 00:20:44.637761+00	f	\N	Spanish	1412adfb-1919-4c80-905b-e0e4cb60d8c0
7675289d-5995-4b4c-8ffc-7a1ec7702771	2021-12-01 00:20:44.637793+00	2021-12-01 00:20:44.637805+00	f	\N	French	1412adfb-1919-4c80-905b-e0e4cb60d8c0
a23054d2-745c-41fc-b83b-0437fdd043ec	2021-12-03 06:14:04.61203+00	2021-12-03 06:14:04.612089+00	f	\N	English	236650ea-d8e1-4b34-b0c6-ddf3d21908c9
dbce0d82-c535-4ffc-94b0-b718f1aae5a4	2021-12-03 06:14:04.612141+00	2021-12-03 06:14:04.612156+00	f	\N	Spanish	236650ea-d8e1-4b34-b0c6-ddf3d21908c9
cad6ab41-06f4-4902-aaf2-e8b638f81956	2021-12-03 06:14:04.612188+00	2021-12-03 06:14:04.612202+00	f	\N	French	236650ea-d8e1-4b34-b0c6-ddf3d21908c9
d401ccc4-a66c-4705-bf5e-61a3a8c3e94f	2021-12-03 10:37:13.356988+00	2021-12-03 10:37:13.357033+00	f	\N	English	fff581d1-3363-43b5-99ae-41830c49a56d
96e4ea8c-d70b-410e-8f93-6ab6a23f4ec0	2021-12-03 10:37:13.357077+00	2021-12-03 10:37:13.357091+00	f	\N	Spanish	fff581d1-3363-43b5-99ae-41830c49a56d
dfbbf3d7-7822-4fc7-b606-dd3664e9b435	2021-12-03 10:37:13.35712+00	2021-12-03 10:37:13.35713+00	f	\N	French	fff581d1-3363-43b5-99ae-41830c49a56d
b9e20fbb-35f0-44a9-bfea-26df291630f2	2021-12-04 17:42:50.401604+00	2021-12-04 17:42:50.401644+00	f	\N	English	afc72cb3-f523-41f0-9934-998199deb882
0c9d6ef7-adc3-4377-8ed1-564f4db99c3e	2021-12-07 12:52:54.172379+00	2021-12-07 12:52:54.172442+00	f	\N	string	39b6fb65-d885-40c7-a8c5-e52904ba264a
26362b31-1ad2-4d1f-b6d4-7a8812c7090a	2021-12-08 04:49:00.768047+00	2021-12-08 04:49:00.768097+00	f	\N	English	1433ed23-9b64-43ad-a0d7-2d1ed6882a4e
6b9e30be-a51f-4a2a-ad78-de5df923d999	2021-12-08 04:49:00.768133+00	2021-12-08 04:49:00.768142+00	f	\N	Spanish	1433ed23-9b64-43ad-a0d7-2d1ed6882a4e
e963b971-0bc6-41fa-9136-0f11e090f30c	2021-12-09 13:15:21.116981+00	2021-12-09 13:15:21.117043+00	f	\N	English	384b0671-0a92-435b-b289-6d59686517b6
54244583-430b-4561-b312-59764993049b	2021-12-09 13:15:21.11709+00	2021-12-09 13:15:21.117101+00	f	\N	Spanish	384b0671-0a92-435b-b289-6d59686517b6
da0e2600-beaf-4b50-a291-c985eb48a240	2021-12-09 13:15:21.11712+00	2021-12-09 13:15:21.117128+00	f	\N	French	384b0671-0a92-435b-b289-6d59686517b6
99b16446-a2d1-40c7-8d44-3a446b409610	2021-12-10 04:42:41.567204+00	2021-12-10 04:42:41.567261+00	f	\N	English	4ef8a711-620e-49cb-85c8-12b6594e7b07
6400f681-0de1-410d-a2f3-cb3710293262	2021-12-17 06:54:47.727972+00	2021-12-17 06:54:47.728019+00	f	\N	English	fc68f79b-79db-439d-958c-b5d8eed2ce02
bf44535f-d4a7-4083-9e8a-2e1bf4ac3632	2021-12-20 18:40:53.760537+00	2021-12-20 18:40:53.760581+00	f	\N	Spanish	4fb7958b-94e4-4354-a641-3023a788ccc1
48eafda0-0945-445c-953c-dc5ecb26c35e	2021-12-22 08:27:02.423431+00	2021-12-22 08:27:02.423471+00	f	\N	English	067f05d0-8a29-4c5c-b070-faa7a0ac9ddc
471e4aed-edbc-4f4d-97c1-b9fd4ab08c3a	2021-12-22 10:18:15.317684+00	2021-12-22 10:18:15.317731+00	f	\N	English	8504ee48-62f2-4f2c-bbb1-b57f65b9f92d
64d70cb1-217a-4f39-8776-35ab828c3cef	2021-12-24 05:15:38.563292+00	2021-12-24 05:15:38.563328+00	f	\N	English	135f16d8-b14c-40cb-a333-787296d86890
\.


--
-- Data for Name: user_doctorreview; Type: TABLE DATA; Schema: public; Owner: sihan
--

COPY public.user_doctorreview (id, created_at, updated_at, is_deleted, deleted_at, patient_name, star_count, comment, doctor_info_id) FROM stdin;
95a38bf6-8efa-49d0-a67c-b9d5f8c27d71	2021-12-23 01:30:55.87097+00	2021-12-23 01:30:55.871024+00	f	\N	Elon Musk	5	Greatest doc. Cured cancer in a day.	4fb7958b-94e4-4354-a641-3023a788ccc1
\.


--
-- Data for Name: user_doctorspecialty; Type: TABLE DATA; Schema: public; Owner: sihan
--

COPY public.user_doctorspecialty (id, created_at, updated_at, is_deleted, deleted_at, specialty, doctor_info_id) FROM stdin;
5a0655b1-3782-4986-ac7f-89708560d912	2021-11-27 07:06:03.559512+00	2021-11-27 07:06:03.559577+00	f	\N	Allergy Specialist	a354ca46-0d86-4f96-8cdb-590a8986513b
e5ba8e73-38c0-436b-8b55-8605e51d536d	2021-11-27 07:06:03.559647+00	2021-11-27 07:06:03.559664+00	f	\N	Anesthesiology	a354ca46-0d86-4f96-8cdb-590a8986513b
f245db2a-bd25-47c1-808a-51ab78e6da4c	2021-11-27 07:07:10.508415+00	2021-11-27 07:07:10.508478+00	f	\N	Anesthesiology	90714f3d-d654-4c8e-b15d-2a08d819f96c
7c417226-5141-4d2a-b690-7e8c5d6762a3	2021-11-27 07:11:48.420069+00	2021-11-27 07:11:48.42013+00	f	\N	Anesthesiology	0440043c-e650-410a-ab98-4fe6ba519ace
08499748-aaa9-4294-889b-95575fca6629	2021-11-30 11:43:25.046143+00	2021-11-30 11:43:25.046187+00	f	\N	Clinical Genetics	46794c6f-add0-496e-83a5-516b922623d0
32bb774d-4624-4f1d-b205-3e673b839444	2021-11-30 11:43:25.046226+00	2021-11-30 11:43:25.046235+00	f	\N	Surgical Oncology	46794c6f-add0-496e-83a5-516b922623d0
1b239f2a-4ad6-4f89-afd4-50ebd98c7de7	2021-11-30 11:43:25.046255+00	2021-11-30 11:43:25.046263+00	f	\N	Neurology	46794c6f-add0-496e-83a5-516b922623d0
4dc065ad-d68b-4949-8300-8fdb1809a289	2021-12-01 00:20:44.625551+00	2021-12-01 00:20:44.625609+00	f	\N	Fitness Expert	1412adfb-1919-4c80-905b-e0e4cb60d8c0
8da0a0f7-e2de-4424-89fc-64440bb0790a	2021-12-01 00:20:44.625667+00	2021-12-01 00:20:44.625683+00	f	\N	Metabolic Surgery	1412adfb-1919-4c80-905b-e0e4cb60d8c0
f5bce554-aa81-4ede-ad0d-69db43ecc816	2021-12-01 00:20:44.625715+00	2021-12-01 00:20:44.625728+00	f	\N	Anesthesiologist/Chronic Pain Specialist	1412adfb-1919-4c80-905b-e0e4cb60d8c0
6f503ec5-4632-41c0-9369-b405a03392a7	2021-12-01 00:20:44.625758+00	2021-12-01 00:20:44.625772+00	f	\N	Pediatric Allergy/Asthma Specialist	1412adfb-1919-4c80-905b-e0e4cb60d8c0
cb56baf0-edea-40a0-bbe1-924dce61363f	2021-12-03 06:14:04.606627+00	2021-12-03 06:14:04.60678+00	f	\N	Andrology	236650ea-d8e1-4b34-b0c6-ddf3d21908c9
2a3a3ecc-a79f-4dce-9c0e-e5d8d354fadf	2021-12-03 06:14:04.606843+00	2021-12-03 06:14:04.606858+00	f	\N	Any Speciality	236650ea-d8e1-4b34-b0c6-ddf3d21908c9
d6d671f6-5597-40fe-b5b8-972cb8d9ac8e	2021-12-03 06:14:04.6069+00	2021-12-03 06:14:04.606913+00	f	\N	Bariatric Surgery	236650ea-d8e1-4b34-b0c6-ddf3d21908c9
294e7ed8-a457-41ab-8e81-7fde5b53a585	2021-12-03 06:14:04.606945+00	2021-12-03 06:14:04.606958+00	f	\N	Endodontist	236650ea-d8e1-4b34-b0c6-ddf3d21908c9
da5b9277-923e-4252-8015-3d0b30fcda8a	2021-12-03 06:14:04.606986+00	2021-12-03 06:14:04.607+00	f	\N	Infectious Diseases	236650ea-d8e1-4b34-b0c6-ddf3d21908c9
a041864c-ffbc-4095-8268-4a8cc26769cd	2021-12-03 10:37:13.352496+00	2021-12-03 10:37:13.352555+00	f	\N	Bariatric Surgery	fff581d1-3363-43b5-99ae-41830c49a56d
d83a4f4e-96b6-4d8a-871c-0bf38c99d025	2021-12-03 10:37:13.352607+00	2021-12-03 10:37:13.352622+00	f	\N	Dermatology	fff581d1-3363-43b5-99ae-41830c49a56d
55bb803e-c9b6-44bf-9858-8e13d308fad5	2021-12-03 10:37:13.352652+00	2021-12-03 10:37:13.352663+00	f	\N	Andrology	fff581d1-3363-43b5-99ae-41830c49a56d
f5754e24-dc5e-4c62-8be0-d537f62f6d62	2021-12-03 10:37:13.352685+00	2021-12-03 10:37:13.352693+00	f	\N	Ayurveda Specialist	fff581d1-3363-43b5-99ae-41830c49a56d
c665a33c-5d3d-489b-bcab-449c365145a3	2021-12-03 10:37:13.352711+00	2021-12-03 10:37:13.352719+00	f	\N	Oral Implantologist	fff581d1-3363-43b5-99ae-41830c49a56d
423b8cdb-7bd7-4677-a8d6-206c3fbff028	2021-12-04 17:42:50.398586+00	2021-12-04 17:42:50.398619+00	f	\N	Child Health	afc72cb3-f523-41f0-9934-998199deb882
4654e0c5-f1ea-4103-b27d-0f091e483acb	2021-12-05 00:31:38.267372+00	2021-12-05 00:31:38.267423+00	f	\N	Child Health	90714f3d-d654-4c8e-b15d-2a08d819f96c
2568270e-021f-47a6-a813-947e51c8db97	2021-12-05 00:54:35.993917+00	2021-12-05 00:54:35.993976+00	f	\N	Chiropractor	90714f3d-d654-4c8e-b15d-2a08d819f96c
ab3260f3-9464-4ad7-88ec-f991d9988c30	2021-12-07 12:52:54.168554+00	2021-12-07 12:52:54.168607+00	f	\N	string	39b6fb65-d885-40c7-a8c5-e52904ba264a
f6eea8d3-f72d-4f24-84e0-e17c9b4e0593	2021-12-08 04:49:00.763176+00	2021-12-08 04:49:00.763221+00	f	\N	Andrology	1433ed23-9b64-43ad-a0d7-2d1ed6882a4e
3dadb908-1e9b-4d01-a53a-7a1cff724667	2021-12-08 04:49:00.763269+00	2021-12-08 04:49:00.763278+00	f	\N	Ayurveda Specialist	1433ed23-9b64-43ad-a0d7-2d1ed6882a4e
89176bce-f445-4a33-8c31-02cc7d15e307	2021-12-08 04:49:00.763297+00	2021-12-08 04:49:00.763304+00	f	\N	Child Health	1433ed23-9b64-43ad-a0d7-2d1ed6882a4e
3d5cbb29-f351-4c83-9102-3eaf62d6f453	2021-12-08 04:49:00.763321+00	2021-12-08 04:49:00.763329+00	f	\N	Childbirth Educator	1433ed23-9b64-43ad-a0d7-2d1ed6882a4e
cf2870ac-c49f-41ff-b968-10df70da5253	2021-12-09 08:50:52.439892+00	2021-12-09 08:50:52.439943+00	f	\N	Andrology	4fb7958b-94e4-4354-a641-3023a788ccc1
773d4589-3625-4cb4-b648-0b5f8b8436b2	2021-12-09 13:15:21.113234+00	2021-12-09 13:15:21.113285+00	f	\N	Family Physician	384b0671-0a92-435b-b289-6d59686517b6
82492309-680d-48ff-8cc6-bc35f5ba0bcf	2021-12-09 13:15:21.113331+00	2021-12-09 13:15:21.113346+00	f	\N	Obstetrics And Gynaecology	384b0671-0a92-435b-b289-6d59686517b6
00cef541-2010-4cd6-b36e-60b724b6520c	2021-12-10 04:42:41.562908+00	2021-12-10 04:42:41.562959+00	f	\N	Anesthesiologist/Chronic Pain Specialist	4ef8a711-620e-49cb-85c8-12b6594e7b07
\.


--
-- Data for Name: user_passwordresetwhitelist; Type: TABLE DATA; Schema: public; Owner: sihan
--

COPY public.user_passwordresetwhitelist (id, created_at, updated_at, is_deleted, deleted_at, email, token) FROM stdin;
\.


--
-- Data for Name: user_patientinfo; Type: TABLE DATA; Schema: public; Owner: sihan
--

COPY public.user_patientinfo (id, created_at, updated_at, is_deleted, deleted_at, gender, date_of_birth, identification_type, identification_number, _identification_photo, insurance_type, insurance_name, insurance_number, insurance_policy_holder_name, referring_doctor_full_name, referring_doctor_phone_number, referring_doctor_address, name_of_parent, user_id, display_id, notification_email) FROM stdin;
a5e1d84b-6365-4d91-a62e-12f9d226a7ca	2021-11-27 06:55:35.752993+00	2021-11-27 06:55:35.767282+00	f	\N	MALE	2021-11-16	PASSPORT	123456	patient_identification_photo/a5e1d84b-6365-4d91-a62e-12f9d226a7ca_2021_11_27_12_55_35_750450.webp	SELF-PAY	\N	\N	\N	Sihan Tawsik	01642518822	32, Abul Khoyrat Road	\N	2a2c60f1-e068-47d2-be66-88bd52116d20	1	\N
b54ff328-3635-4084-a160-e1e98f65b47e	2021-11-27 06:57:28.189318+00	2021-12-23 12:37:30.421096+00	f	\N	MALE	2021-11-16	PASSPORT	123456	patient_identification_photo/b54ff328-3635-4084-a160-e1e98f65b47e_2021_11_27_12_57_28_187855.webp	SELF-PAY	\N	\N	\N	Sihan Tawsik	01642518822	32, Abul Khoyrat Road	\N	876b4dde-d1f6-4e79-a513-b7375b2b954c	2	user@example.com
2b59a0f4-1707-482f-bcb8-2793a300b390	2021-11-27 06:58:04.896044+00	2021-11-27 06:58:04.907165+00	f	\N	MALE	2021-11-16	PASSPORT	123456	patient_identification_photo/2b59a0f4-1707-482f-bcb8-2793a300b390_2021_11_27_12_58_04_894819.webp	SELF-PAY	\N	\N	\N	Sihan Tawsik	01642518822	32, Abul Khoyrat Road	\N	ed76b722-e7f8-46cd-8dff-f4f687856bf3	3	\N
e642db21-9ca3-48e0-9b1b-137917cd6dac	2021-11-30 12:32:08.617954+00	2021-11-30 12:32:08.634424+00	f	\N	MALE	2021-12-01	PASSPORT	3479738523872	patient_identification_photo/e642db21-9ca3-48e0-9b1b-137917cd6dac_2021_11_30_18_32_08_612996.jpeg	SELF-PAY	\N	\N	\N	r name	236468232	r test address	\N	b92072ba-b707-4da1-89bc-0c16e4b65634	4	\N
a4b77d55-4b7b-46ae-8fed-c2be186120a0	2021-12-01 00:19:19.906206+00	2021-12-01 00:19:19.91167+00	f	\N	MALE	2021-12-01	PASSPORT	3479738523872	patient_identification_photo/a4b77d55-4b7b-46ae-8fed-c2be186120a0_2021_12_01_06_19_19_901853.jpeg	SELF-PAY	\N	\N	\N	r name	236468232	r test address	\N	554b90e7-9846-4d91-baec-c5848702fb26	6	\N
52139077-520d-476b-b1d9-7db63829da2b	2021-12-01 08:16:41.064502+00	2021-12-01 08:16:41.070411+00	f	\N	MALE	2021-12-01	DRIVER'S LICENSE	dasdasd	patient_identification_photo/52139077-520d-476b-b1d9-7db63829da2b_2021_12_01_14_16_41_060375.png	SELF-PAY	\N	\N	\N	asdasd	asdasd	asdasdasd	\N	4fd98941-ef2f-4812-b7e1-3b707fb6140c	7	\N
d248170b-5d9d-48c9-9688-cbccdd39162a	2021-12-02 04:36:11.684698+00	2021-12-02 04:36:11.689913+00	f	\N	MALE	2021-12-02	PASSPORT	3479738523872	patient_identification_photo/d248170b-5d9d-48c9-9688-cbccdd39162a_2021_12_02_10_36_11_679399.jpeg	SELF-PAY	\N	\N	\N	r name	236468232	r test address	\N	b800d6d5-deb5-4e73-806a-1a85070662f2	8	\N
b20eb1b6-180a-4ef5-ab36-9b5a5c39ea2c	2021-12-03 08:55:37.887221+00	2021-12-03 08:55:37.898315+00	f	\N	FEMALE	2000-01-05	DRIVER'S LICENSE	DL02194	patient_identification_photo/b20eb1b6-180a-4ef5-ab36-9b5a5c39ea2c_2021_12_03_14_55_37_883816.jpeg	INSURANCE	Cigna	CIG00001	self	ELiz Ola	3338902901	123 Main Street	\N	49dbba2e-f487-4c5c-aa4b-3964d34b6711	9	\N
158904c9-d1a7-4a74-9599-783f541bf9eb	2021-12-03 10:25:46.095314+00	2021-12-03 10:25:46.099197+00	f	\N	MALE	2021-12-03	PASSPORT	3479738523872	patient_identification_photo/158904c9-d1a7-4a74-9599-783f541bf9eb_2021_12_03_16_25_46_093109.jpeg	SELF-PAY	\N	\N	\N	r name	236468232	r test address	\N	10210419-bb1d-4192-af63-77fc3b86fa4a	10	\N
eb4b97d4-c265-4466-aa77-8628b7973cc8	2021-12-03 10:35:18.919581+00	2021-12-03 10:35:18.92317+00	f	\N	MALE	1995-09-27	DRIVER'S LICENSE	135673890	patient_identification_photo/eb4b97d4-c265-4466-aa77-8628b7973cc8_2021_12_03_16_35_18_917423.jpeg	SELF-PAY	\N	\N	\N	r name	236468232	r test address	\N	b75bc244-cd62-4d39-b257-2820aa43eeb8	11	\N
fef7b31d-603f-45c3-8155-634745a4d655	2021-12-04 17:37:50.467066+00	2021-12-04 17:37:50.471055+00	f	\N	MALE	1992-11-01	PASSPORT	219401688	patient_identification_photo/fef7b31d-603f-45c3-8155-634745a4d655_2021_12_04_23_37_50_463236.png	SELF-PAY	\N	\N	\N	shafayat	124308647	address	\N	7765be45-f16d-41a0-b1a1-24498b59eeac	12	\N
1d25e38a-63bb-4b41-8d25-8e882eff28b2	2021-12-07 03:05:59.445929+00	2021-12-07 03:05:59.451299+00	f	\N	MALE	1991-12-07	PASSPORT	98298357287382	patient_identification_photo/1d25e38a-63bb-4b41-8d25-8e882eff28b2_2021_12_07_09_05_59_443069.png	SELF-PAY	Hi	a1nmsdjdn1e38hnjd	Hiihihi	No doctor	012929832938	abc@example.com	Abul Kashem	c815552a-0f4b-48da-a871-f86a4ed15268	13	\N
a684a31d-05ee-48af-9186-5b2d22453fc3	2021-12-08 04:58:09.829097+00	2021-12-08 04:58:09.833718+00	f	\N	MALE	2021-12-08	DRIVER'S LICENSE	test_12123	patient_identification_photo/a684a31d-05ee-48af-9186-5b2d22453fc3_2021_12_08_10_58_09_824848.png	SELF-PAY	\N	\N	\N	Samnan Rahee	+8801521436367	236/c, vuianpara, sipahibag, khilgaon	\N	53f3d1ab-6ef4-423f-abbe-2f502d021ac0	14	\N
54647792-a94b-4911-bf9a-82bffc07f02a	2021-12-09 10:02:08.35887+00	2021-12-09 10:02:08.363669+00	f	\N	FEMALE	1999-01-01	DRIVER'S LICENSE	D08976	patient_identification_photo/54647792-a94b-4911-bf9a-82bffc07f02a_2021_12_09_16_02_08_354716.jpeg	INSURANCE	Cigna	CIG00001	Self	Dr Richards	9736789056	129 Main Street, Avondale, NJ 07098	\N	5d454090-2584-4953-852c-c6a0e2c2d30e	15	\N
69283ecd-a348-481f-8acd-c9de320cad0e	2021-12-10 04:45:22.821822+00	2021-12-10 04:45:22.824707+00	f	\N	FEMALE	2003-12-09	DRIVER'S LICENSE	1111111	patient_identification_photo/69283ecd-a348-481f-8acd-c9de320cad0e_2021_12_10_10_45_22_819260.png	SELF-PAY	\N	\N	\N	Sanviraj Zahin Haque	01521435473	Masdair Gudaraghat	\N	74df4c91-61c9-4d1f-8c5e-05fef52eecf9	16	\N
138ee561-527f-4024-974b-ef30b52237be	2021-12-10 14:53:01.25126+00	2021-12-10 14:53:01.259256+00	f	\N	FEMALE	2000-01-01	PASSPORT	wgesreg	patient_identification_photo/138ee561-527f-4024-974b-ef30b52237be_2021_12_10_20_53_01_246934.png	SELF-PAY	\N	\N	\N	\N	\N	\N	\N	a0312245-e73a-4763-9a27-5a2aba93cda3	17	\N
b3c268ee-91d3-4227-a6ee-6e63babd107d	2021-12-14 08:47:24.423653+00	2021-12-14 08:47:24.427896+00	f	\N	FEMALE	1999-07-14	STATE ID	111233	patient_identification_photo/b3c268ee-91d3-4227-a6ee-6e63babd107d_2021_12_14_14_47_24_421163.png	SELF-PAY	\N	\N	\N	\N	\N	\N	\N	235a9a51-9ceb-4b55-a687-46bc634eb0fa	18	\N
8110e5dc-3917-4567-abda-9bb4eed19ad4	2021-12-23 05:34:35.320744+00	2021-12-23 05:34:35.323757+00	f	\N	MALE	2003-12-04	PASSPORT	43553363663	patient_identification_photo/8110e5dc-3917-4567-abda-9bb4eed19ad4_2021_12_23_11_34_35_318389.png	SELF-PAY	\N	\N	\N	\N	\N	\N	\N	76d927d5-9b1d-4418-badd-a970cbf72c88	19	\N
3f24bf6d-9bac-4b7e-9027-035fa0ed66c3	2021-12-25 10:18:44.531138+00	2021-12-25 10:18:44.533676+00	f	\N	MALE	2003-01-01	STATE ID	122122	patient_identification_photo/3f24bf6d-9bac-4b7e-9027-035fa0ed66c3_2021_12_25_16_18_44_529666.jpeg	SELF-PAY	\N	\N	\N	\N	\N	\N	\N	6c0e20bd-57f4-48e6-a2bf-75319fef2cf3	20	\N
\.


--
-- Data for Name: user_pharmacyinfo; Type: TABLE DATA; Schema: public; Owner: sihan
--

COPY public.user_pharmacyinfo (id, created_at, updated_at, is_deleted, deleted_at, username, number_of_practitioners, user_id, notification_email) FROM stdin;
d837b959-c3eb-4733-b41c-60e327aea644	2021-11-27 07:27:20.438339+00	2021-11-27 07:27:20.438396+00	f	\N	pro	0	b082a946-48ab-4391-84f6-3892814e0f3a	\N
86ecbc9f-97f8-4dd2-8dc2-1836e1fe43c8	2021-11-28 02:51:37.28038+00	2021-11-28 02:51:37.280428+00	f	\N	pro.1	0	4dfe08bf-0e1a-41a5-9e25-02c0ad512c4b	\N
32fdff57-d8d5-42a5-b69f-dab5020759e3	2021-11-28 02:53:56.978257+00	2021-11-28 02:53:56.978302+00	f	\N	pro.2	0	e5bbcb5a-deef-46d5-9226-1fbb9b7398c8	\N
f41a9a90-efb5-4dd4-b998-0c0c2bac60d1	2021-11-30 08:22:22.693498+00	2021-11-30 08:22:22.693598+00	f	\N	jason’s.pharmacy	0	1c2c6aa1-90b0-475a-a95a-6d396e0f2bda	\N
751529ba-8be1-414f-84f0-bbbafd8bfa7a	2021-12-03 07:09:07.297979+00	2021-12-03 07:09:07.298173+00	f	\N	pharmacy_giri	0	69563331-2401-4acb-98e3-4089f7298f45	\N
a1c4df9f-b62a-4806-8c49-873be31d881d	2021-12-08 05:35:17.559073+00	2021-12-08 05:35:17.559126+00	f	\N	samnan.rahee	0	74096425-92ab-49d7-ad1a-c35b355e3260	\N
e54ace41-9aa3-413a-9948-8e2e99ddd997	2021-12-14 19:19:15.979198+00	2021-12-27 06:55:15.177967+00	f	\N	fahin-pharmacy	0	db3fc55b-bd76-4ce6-9874-170ab76870ca	testingdokto@gmail.com
cd51a75f-bb0f-4a15-9d3c-9520ea3937e6	2021-12-15 07:30:08.087652+00	2021-12-15 07:30:08.087738+00	f	\N	sihan-tawsik-pharmacy	0	121f7441-6453-455e-ab9c-4b50a64ecf66	\N
0740825a-145f-49c2-94f1-fe112033a1e8	2021-12-17 16:00:15.305408+00	2021-12-17 16:00:15.305523+00	f	\N	klik-pharmacy	0	1d5b7522-c466-4bec-85f4-943ee6ae16c6	\N
6edafe91-d9e8-498f-8ccf-1780cb4970cb	2021-12-22 06:22:48.390905+00	2021-12-22 06:22:48.390946+00	f	\N	oyetayo-tosin-tunde	0	7c52ea4a-efb3-4d4e-804f-e9bd2049cafa	\N
3f715672-5222-4fbb-8e55-2dc2ccf93df1	2021-12-27 07:21:13.644465+00	2021-12-27 07:21:13.644499+00	f	\N	meh	0	f23ba24b-665e-4e01-8b9a-85cda57e4ad1	\N
\.


--
-- Data for Name: user_user; Type: TABLE DATA; Schema: public; Owner: sihan
--

COPY public.user_user (password, last_login, is_superuser, is_staff, is_active, date_joined, id, created_at, updated_at, is_deleted, deleted_at, full_name, email, user_type, is_verified, street, state, city, zip_code, contact_no, _profile_photo) FROM stdin;
pbkdf2_sha256$260000$M4juFXMO2p1DjPHcNPfh2v$dn+Mk4wjKvqFLzZx7McPoRwnIa+fLmWAt7D1hePKKqY=	\N	f	f	t	2021-11-27 06:55:35.685009+00	2a2c60f1-e068-47d2-be66-88bd52116d20	2021-11-27 06:55:35.685996+00	2021-12-23 11:41:25.857119+00	f	\N	pat s ahmed	saad.akash.dev@gmail.com	PATIENT	f	32, Abul Khoyrat Road	Central Region	\N	1100	88001642518822	profile_photo/2a2c60f1-e068-47d2-be66-88bd52116d20_2021_11_27_12_55_35_704584.webp
pbkdf2_sha256$260000$bMn8NsvWFuTtTRWOeDtLB7$LIa/3lzmAAVwTGWoCJZaizJYqKmJGS7WMgKoFs3jrhY=	\N	f	f	t	2021-11-27 06:57:28.146315+00	876b4dde-d1f6-4e79-a513-b7375b2b954c	2021-11-27 06:57:28.147552+00	2021-12-23 12:58:05.877236+00	f	\N	Test Patient	patient@dokto.com	PATIENT	f	32, Abul Khoyrat Road	Central Region	\N	1100	88001642518822	
pbkdf2_sha256$260000$2MpMOIDHxbrQz06ND1WRNi$1nIHku8zzw9rVGdUBuiWE+hIGn51boDr7/3+qfUeorY=	\N	f	f	t	2021-11-27 06:58:04.856158+00	ed76b722-e7f8-46cd-8dff-f4f687856bf3	2021-11-27 06:58:04.856897+00	2021-12-21 11:46:30.848736+00	f	\N	patient dokto	sihan@patient.com	PATIENT	f	32, Abul Khoyrat Road	Central Region	\N	1100	88001642518822	profile_photo/ed76b722-e7f8-46cd-8dff-f4f687856bf3_2021_11_27_12_58_04_870994.webp
pbkdf2_sha256$260000$pjmR04yKzYX9BM0BH1ISL7$ajwUGFhOz3axsgn2cJ1iEUwWQd8pvW9LwawBO34b8Fg=	\N	f	f	t	2021-11-27 07:06:03+00	09a95982-a373-4555-9347-b963628701ac	2021-11-27 07:06:03.211469+00	2021-12-20 13:18:08.666818+00	f	\N	Sanviraj Zahin Haque	zahinjason220434@gmail.com	DOCTOR	t	Masdair Gudaraghat	Plav Municipality	Azimpur	1400	88001521435473	
pbkdf2_sha256$260000$NL0hs4rmDHdq32J9QsqBLh$y5K24kDB6SdfjUyj7KAXcvL8IF5dqiEJaRLFtBd+F58=	\N	f	f	t	2021-11-27 07:07:10.253935+00	1dd1ffe0-2113-4c97-bcf2-abe2798bba3d	2021-11-27 07:07:10.254887+00	2021-12-22 08:04:47.776813+00	f	\N	Dr Saad Ahmed Akash	sa.akash0129@gmail.com	DOCTOR	f	32, Abul Khoyrat Road	Central Region	\N	1100	88001642518822	
pbkdf2_sha256$260000$pGrkqk5pKJL9nAuISLd9dc$3RAPLhQvsXoH+1I3CYuf+uUfE5iMY2wvC9PQD1PGXbM=	\N	f	f	t	2021-11-27 07:11:07+00	952478f7-4c6e-497a-b6c0-7f11ca93ae12	2021-11-27 07:11:07.957657+00	2021-12-27 07:22:54.363323+00	t	\N	Mahmudul Alam	mahmudul@dokto.com	DOCTOR	f	32, Abul Khoyrat Road	Central Region	Dhaka	1100	88001642518822	profile_photo/952478f7-4c6e-497a-b6c0-7f11ca93ae12_2021_12_21_16_10_36_504700.jpeg
pbkdf2_sha256$260000$VpOS50EaxFSCRHmrjuQI3w$h04+kDQiWU1hNnFT3qXZvfAdhSpd18Z7JHZjr2Tdvew=	\N	f	f	t	2021-11-27 07:11:48.282954+00	3a0edd9f-747f-4c4d-b271-bc6b38696fe4	2021-11-27 07:11:48.283617+00	2021-12-20 12:57:35.310065+00	f	\N	sihan	sihan@dokto.com	DOCTOR	f	32, Abul Khoyrat Road	Central Region	\N	1100	88001642518822	
pbkdf2_sha256$260000$T4CQL3SBEtdpJaZWlAe1MS$gDwsnwsgMoQb0Lidi+PSRjweEG4kqodscLoxf4CMo3I=	\N	f	f	t	2021-11-27 07:27:20.398223+00	b082a946-48ab-4391-84f6-3892814e0f3a	2021-11-27 07:27:20.39893+00	2021-11-27 07:27:20.425738+00	f	\N	pro	pro@gmail.com	PHARMACY	f	12/A	Luqa	Constantine	672	3551845435118	profile_photo/b082a946-48ab-4391-84f6-3892814e0f3a_2021_11_27_13_27_20_410304.png
pbkdf2_sha256$260000$0luIOeEW87C9eLt6VgsKUN$20TTE3Cm4P/NVrMcTJHTG5+WKXWzo0NIPj8S7PnyteI=	\N	f	f	t	2021-11-27 08:26:59.383578+00	77ffd331-ced9-46e1-947c-d445565eecce	2021-11-27 08:26:59.384361+00	2021-11-27 08:26:59.398706+00	f	\N	Prodipta Banerjee	probanerjee17@gmail.com	CLINIC	f	savar	Bar Municipality	\N	2011	97303234234	profile_photo/77ffd331-ced9-46e1-947c-d445565eecce_2021_11_27_14_26_59_389900.png
pbkdf2_sha256$260000$G5N1E1WmwZZPo2tTao25nc$3ou5f4UwU8XTkZnsO5p8yVgGXjf3/22vIXBhRPhDfhY=	\N	f	f	t	2021-11-28 02:51:37.263623+00	4dfe08bf-0e1a-41a5-9e25-02c0ad512c4b	2021-11-28 02:51:37.264328+00	2021-11-28 02:51:37.276605+00	f	\N	pro	proexample@gmail.com	PHARMACY	f	12/A	Plav Municipality	Gopalganj	672	8801845435118	profile_photo/4dfe08bf-0e1a-41a5-9e25-02c0ad512c4b_2021_11_28_08_51_37_267759.png
pbkdf2_sha256$260000$ET57iPPpwJQckSviSH8jZF$E/dDPWoA6TxZ/xeHv8F4gGahcNL00asYJMSfwRYcqhI=	\N	f	f	t	2021-11-28 02:53:56.957663+00	e5bbcb5a-deef-46d5-9226-1fbb9b7398c8	2021-11-28 02:53:56.958224+00	2021-11-28 02:53:56.97288+00	f	\N	pro	timekiller1727@gmail.com	PHARMACY	f	12/A	Plav Municipality	Sayani	672	8801845435118	profile_photo/e5bbcb5a-deef-46d5-9226-1fbb9b7398c8_2021_11_28_08_53_56_964975.png
pbkdf2_sha256$260000$B8qWP1Wj7ryQK77oZ5D3K0$BWyr0zbKUaZVNVQ+Q9n0EABmq0Wbv850fP4PnV90ngQ=	2021-12-20 13:06:16.72273+00	t	t	t	2021-11-28 07:56:19.481888+00	25482094-6737-4177-b465-9a179fd5602d	2021-11-28 07:56:19.482475+00	2021-11-28 07:56:19.482488+00	f	\N		admin@dokto.com	ADMIN	f	\N	\N	\N	\N	\N	
pbkdf2_sha256$260000$EFrlrXOLboJvJvU5rQDTr7$d/Qv5lZCcLcvNZdP4HPtcjRJjsnwlrvKY1h7fU+nieM=	\N	f	f	t	2021-11-28 08:15:39.180767+00	c5ce351d-b516-4a27-b62a-30eb1ec98025	2021-11-28 08:15:39.181416+00	2021-11-28 08:15:39.19664+00	f	\N	pro	pro123@gmail.com	CLINIC	f	12/A	Sliema	\N	672	8801845435118	profile_photo/c5ce351d-b516-4a27-b62a-30eb1ec98025_2021_11_28_14_15_39_187298.png
pbkdf2_sha256$260000$DWpzjZngFIFwlD8cYbfG3q$iYo5Ia/en8398gdv/AO3/DLUoUaIFiV1rJrpIRHLPIA=	\N	f	f	t	2021-11-29 05:26:53.751145+00	17e97df5-162c-45ec-a190-79626b980f4b	2021-11-29 05:26:53.751933+00	2021-11-29 05:26:53.77087+00	f	\N	Random	sdadsasd@email.co	CLINIC	f	236/c, vuianpara, sipahibag, khilgaon	Central Region	\N	1100	880+8801521436367	profile_photo/17e97df5-162c-45ec-a190-79626b980f4b_2021_11_29_11_26_53_757162.png
pbkdf2_sha256$260000$mRKwTqWaXofp7TWmBSuw2j$oKsZOPKpMULgsaBGjKWyvD8qKqtxFd7b2+ZPSZADnCw=	\N	f	f	t	2021-11-29 08:27:24.660274+00	f0eb657a-57e3-4d10-b336-8523c5a02050	2021-11-29 08:27:24.661043+00	2021-11-29 08:27:24.680057+00	f	\N	St Marys Hospital	pejute@yahoo.com	CLINIC	f	22 GOULD ROAD, LORDSWOOD	Kent	\N	ME5 8EA	99407948320303	profile_photo/f0eb657a-57e3-4d10-b336-8523c5a02050_2021_11_29_14_27_24_666188.png
pbkdf2_sha256$260000$neONgW7f9qvQBoVD5A3bUC$t/uwNKsv3mnynD9EfoX+3gn1teR+1b8cv2j/VtFfZB0=	\N	f	f	t	2021-11-30 05:37:57.621858+00	633420fb-e20c-4deb-8162-bedcd3d92c68	2021-11-30 05:37:57.622682+00	2021-11-30 05:37:57.633365+00	f	\N	L hospital	zahin1123455@gmail.com	CLINIC	f	afghan road	Ghazni	Ghazni	1400	931111111	profile_photo/633420fb-e20c-4deb-8162-bedcd3d92c68_2021_11_30_11_37_57_627431.jpeg
pbkdf2_sha256$260000$xhLvat2vuNZFBZBVQrNvus$nBqQv7oLTasRP76DVBMQHps+yoB+zHSFhShRGGwk3Kg=	\N	f	f	t	2021-11-30 05:39:51.129588+00	c739b88f-ffa9-4e03-9a5f-f9064b472b65	2021-11-30 05:39:51.130411+00	2021-11-30 05:39:51.144938+00	f	\N	L hospital	newEmailForJason1163@gmail.com	CLINIC	f	afghan road	Ghazni	Ghazni	1400	931111111	profile_photo/c739b88f-ffa9-4e03-9a5f-f9064b472b65_2021_11_30_11_39_51_134799.jpeg
pbkdf2_sha256$260000$Znxpirpjt7dvQHSEonmEkN$XO2tthmE0MUPMs6cgUajLT8hGCJcRzi+xEmqR2T6vFw=	\N	f	f	t	2021-11-30 05:43:57.602594+00	c1f9bc20-8e97-4e7a-b2a1-2419ede06191	2021-11-30 05:43:57.603195+00	2021-11-30 05:43:57.611622+00	f	\N	new hospital	szh220434@gmail.com	CLINIC	f	Address	Ghazni	Ghazni	100	931103455	profile_photo/c1f9bc20-8e97-4e7a-b2a1-2419ede06191_2021_11_30_11_43_57_606444.jpeg
pbkdf2_sha256$260000$qrjbuOuw6Rkypahxceabyd$3HS7lb27NW/mpbEB31PVUhsnP9+gbNglA2Ye7E1wLHk=	\N	f	f	t	2021-11-30 05:46:32.781249+00	bddf4b1e-3a5b-4f13-a89f-c43b79d9cfde	2021-11-30 05:46:32.781892+00	2021-11-30 05:46:32.799763+00	f	\N	Jason’s hospital	zahinjason5580@gmail.com	CLINIC	f	afghan rod	Ghazni	Ghazni	100	93567890	profile_photo/bddf4b1e-3a5b-4f13-a89f-c43b79d9cfde_2021_11_30_11_46_32_786364.jpeg
pbkdf2_sha256$260000$1BwXVXWfgzi5ZMOO1xKOQ3$2QhtyRijREtuOVsSLWkXVh/4g5UNjkHoOW91ehL+f58=	\N	f	f	t	2021-11-30 05:49:09.480861+00	245b2b72-4fae-40ac-bab1-f3cfc0f70c42	2021-11-30 05:49:09.481479+00	2021-11-30 05:49:09.491664+00	f	\N	hospital	gokunoui@gmail.com	CLINIC	f	hehe	Ghazni	Ghazni	100	93123456789	profile_photo/245b2b72-4fae-40ac-bab1-f3cfc0f70c42_2021_11_30_11_49_09_486643.jpeg
pbkdf2_sha256$260000$6GnYEwRZF9zspT6I4vPT3x$eKAgXqPlh78CKeRsZCX5hP2zLmcIKHLFCdvXOCGW4eU=	\N	f	f	t	2021-11-30 05:53:33.201688+00	91d1b59d-b202-486a-bfcc-d9c0490a88f7	2021-11-30 05:53:33.202312+00	2021-11-30 05:53:33.215038+00	f	\N	hospital	sanviraj.z.haque@gmail.com	CLINIC	f	heheh	Ghazni	Ghazni	12345	931234567	profile_photo/91d1b59d-b202-486a-bfcc-d9c0490a88f7_2021_11_30_11_53_33_206828.jpeg
pbkdf2_sha256$260000$xTNSq7o0ThPXyH7S85KwLu$+xQfE1DztgsJdPOgQTm7Z893THd5GwlDQFaCIDeE8fs=	\N	f	f	t	2021-11-30 06:33:34.708978+00	dd7346c1-32db-48dd-8274-c4eca960836c	2021-11-30 06:33:34.709511+00	2021-11-30 06:33:34.71775+00	f	\N	hospital	thisisatestzahin2222@gmail.com	CLINIC	f	address	Ghazni	Ghazni	1000	93123456789	profile_photo/dd7346c1-32db-48dd-8274-c4eca960836c_2021_11_30_12_33_34_713062.jpeg
pbkdf2_sha256$260000$ZgyfMqFIqNAqg6LSo957IM$BAEdpWtcnGPf0HxxDCJlMAiQu53ZrPFZpingt3YpK0k=	\N	f	f	t	2021-11-30 06:45:08.429644+00	88efdf2d-bec2-4221-9196-a11ef2391bd3	2021-11-30 06:45:08.430423+00	2021-11-30 06:45:08.45265+00	f	\N	hehe hospital	hehe@gmail.com	CLINIC	f	hehe	Ghazni	Ghazni	1000	931234789	profile_photo/88efdf2d-bec2-4221-9196-a11ef2391bd3_2021_11_30_12_45_08_440430.jpeg
pbkdf2_sha256$260000$fKiI1oD8OiatxqvDFNraCH$rWoSZjSU9go4viTrzYfXLt/QL7Y/vZyhqJXkeXu5Pm0=	\N	f	f	t	2021-11-30 06:47:33.345502+00	a2d0ca75-c7b0-4ccd-bdcb-9fcfd76db504	2021-11-30 06:47:33.346201+00	2021-11-30 06:47:33.359076+00	f	\N	hehe hospital	hehepiamon@gmail.com	CLINIC	f	195	Ghazni	Ghazni	100	939865373	profile_photo/a2d0ca75-c7b0-4ccd-bdcb-9fcfd76db504_2021_11_30_12_47_33_352099.jpeg
pbkdf2_sha256$260000$EFhpZe2WFOQuv73mYGbD77$R2XMBiiDR3aS9MElhFkUKFCH+GG4BiYI9FeSGoDzExc=	\N	f	f	t	2021-11-30 06:50:52.713987+00	cbff03a1-de8f-4f06-be55-6689d56b5c91	2021-11-30 06:50:52.714459+00	2021-11-30 06:50:52.723313+00	f	\N	hospital keys khulsi	edotenseigan@gmail.com	CLINIC	f	Afghan colony	Ghazni	Ghazni	1000	93123983	profile_photo/cbff03a1-de8f-4f06-be55-6689d56b5c91_2021_11_30_12_50_52_717693.jpeg
pbkdf2_sha256$260000$4h74hQ11wfBBESHBSR8Anc$aHhMmdzciG8RWn8D2bB1IamS8eSzLKhYvS69x9T4Z5M=	\N	f	f	t	2021-11-30 06:53:36.537194+00	8c268125-2199-4272-ad77-6e857678702a	2021-11-30 06:53:36.538107+00	2021-11-30 06:53:36.558258+00	f	\N	hospital keys noting	email@rmail.com	CLINIC	f	address	Ghazni	Ghazni	100	931238883	profile_photo/8c268125-2199-4272-ad77-6e857678702a_2021_11_30_12_53_36_551402.jpeg
pbkdf2_sha256$260000$928AC55fjWNUR9MbnNkbt7$Wz/mFK/EoztCzbYO+d2QfSXMyj1prlkn54YTiRDmhDw=	\N	f	f	t	2021-11-30 06:57:04.474196+00	75a74960-1352-4fc4-97a8-eba612426c7c	2021-11-30 06:57:04.475058+00	2021-11-30 06:57:04.488501+00	f	\N	Jason Baha’i we	emali@gmali.com	CLINIC	f	afghan I polao	Ghazni	Ghazni	1000	9312378474	profile_photo/75a74960-1352-4fc4-97a8-eba612426c7c_2021_11_30_12_57_04_480459.jpeg
pbkdf2_sha256$260000$jRKMLhhUvJw6nKh7UzOyIs$epd5t4KuUS3A9n9qAQpG9xhOiz88gucRgWzzePwtXh8=	\N	f	f	t	2021-11-30 08:02:13.257874+00	4ebfc00b-4b4a-442a-b135-782bcc6b112e	2021-11-30 08:02:13.25863+00	2021-11-30 08:02:13.274716+00	f	\N	lama hospital	lamamammamam@gmaila.com	CLINIC	f	Idaho street	Ghazni	Ghazni	900	937837373	profile_photo/4ebfc00b-4b4a-442a-b135-782bcc6b112e_2021_11_30_14_02_13_268359.jpeg
pbkdf2_sha256$260000$qTmNg6AKwNt3EpUHRiXB0m$YFam10GVQ5x2NDkdRAiIflQsD2TNn8GKPxLhZJCDVgQ=	\N	f	f	t	2021-11-30 08:05:25.534554+00	35c8c822-025c-4342-8fb0-424af92b2cc8	2021-11-30 08:05:25.535074+00	2021-11-30 08:05:25.551804+00	f	\N	hehe hospital	email@jason.com	CLINIC	f	address	Ghazni	Ghazni	100	938938833	profile_photo/35c8c822-025c-4342-8fb0-424af92b2cc8_2021_11_30_14_05_25_546770.jpeg
pbkdf2_sha256$260000$7o4JyrsiiMTXSNJrRpAV56$6v4I5OnCgGvWljIPS2/KTgZKYLLlqel/fIT3kwBcFgE=	\N	f	f	t	2021-11-30 08:22:22.668733+00	1c2c6aa1-90b0-475a-a95a-6d396e0f2bda	2021-11-30 08:22:22.669499+00	2021-11-30 08:22:22.684474+00	f	\N	Jason’s Pharmacy	afiatamanna06@gmail.com	PHARMACY	f	hehe land	Ghazni	Ghazni	12345	93128228282	profile_photo/1c2c6aa1-90b0-475a-a95a-6d396e0f2bda_2021_11_30_14_22_22_674329.jpeg
pbkdf2_sha256$260000$E2ns5RVFRo6sY34TPQkEgN$tdaA1vgcaiu1cNRkOejRcBgHmN4niFyElNSrZdEu4mU=	\N	f	f	t	2021-11-30 11:43:24.996869+00	a81869fe-3d7e-4a82-b9a7-239311c5c5a2	2021-11-30 11:43:24.997495+00	2021-11-30 11:43:25.006701+00	f	\N	Full name	test1@test.com	DOCTOR	f	test address	Dhaka Division	Dhaka	1212	1913243746	profile_photo/a81869fe-3d7e-4a82-b9a7-239311c5c5a2_2021_11_30_17_43_25_001655.jpeg
pbkdf2_sha256$260000$T67Cx5hzCd5VVKchyN1rFH$+VadLR6NYbQGLj7hNhTKMZSZ9blfwZ4GNZ1JAVrsIPQ=	\N	f	f	t	2021-11-30 12:32:08.592068+00	b92072ba-b707-4da1-89bc-0c16e4b65634	2021-11-30 12:32:08.592789+00	2021-11-30 12:32:08.605285+00	f	\N	First name Last name	test@test.com	PATIENT	f	test address	Bangladesh	Dhaka	1212	1913243746	profile_photo/b92072ba-b707-4da1-89bc-0c16e4b65634_2021_11_30_18_32_08_597882.jpeg
pbkdf2_sha256$260000$ZAAmGPM1oQRMLcdgtJc0Oa$Swtx/evMNWZ3eLhfa6fZISzmHASS+pL8Pt7YnmZW8p4=	\N	f	f	t	2021-12-01 00:19:19.883092+00	554b90e7-9846-4d91-baec-c5848702fb26	2021-12-01 00:19:19.883824+00	2021-12-01 00:19:19.896699+00	f	\N	First name Last name	test@testy.com	PATIENT	f	test address	Bangladesh	Dhaka	1212	1913243746	profile_photo/554b90e7-9846-4d91-baec-c5848702fb26_2021_12_01_06_19_19_890285.jpeg
pbkdf2_sha256$260000$50wfjxPSNVS3uo5BfCgyvl$ttwLQbYEYVZEUlTU4n83vLFaFRfGbXgZwdvWdQIKJ5o=	\N	f	f	t	2021-12-01 00:20:44.523893+00	969142a9-3a26-45f1-952e-6ec5d0e6fa1a	2021-12-01 00:20:44.524805+00	2021-12-01 00:20:44.539999+00	f	\N	Full name	test1@testii.com	DOCTOR	f	test address	Dhaka Division	Dhaka	1212	1913243746	profile_photo/969142a9-3a26-45f1-952e-6ec5d0e6fa1a_2021_12_01_06_20_44_530156.jpeg
pbkdf2_sha256$260000$Uih36YxXWFA7AvOX9woXfS$GTyCzoi4F6cUu0YB6uJjXGCrZCRnKTR36c2+eBnRUmU=	\N	f	f	t	2021-12-01 08:16:41.034185+00	4fd98941-ef2f-4812-b7e1-3b707fb6140c	2021-12-01 08:16:41.035055+00	2021-12-01 08:19:52.078517+00	f	\N	Samnan Rahee	samnan.rahee.96@gmail.com	PATIENT	t	236/c, vuianpara, sipahibag, khilgaon	Kogi State	\N	1100	93asdasdsd	profile_photo/4fd98941-ef2f-4812-b7e1-3b707fb6140c_2021_12_01_14_16_41_040099.png
pbkdf2_sha256$260000$h8E1AqUvEaVZaVAPiIkaqP$EWNRXxyP6NXcKXVdR3a+dwE66LrS2q4g9odzcVlSFHw=	\N	f	f	t	2021-12-02 04:36:11.652163+00	b800d6d5-deb5-4e73-806a-1a85070662f2	2021-12-02 04:36:11.653294+00	2021-12-02 04:36:11.673602+00	f	\N	First name Last name	testingdata@test.com	PATIENT	f	test address	Bangladesh	Dhaka	1212	1913243746	profile_photo/b800d6d5-deb5-4e73-806a-1a85070662f2_2021_12_02_10_36_11_663220.jpeg
pbkdf2_sha256$260000$p8ddkcFlQl7FMgAkASQ36m$r0sNHd9XGqcxsrFRFb4lylwuKkkTB4k25gtGCU4Uq8s=	\N	f	f	t	2021-12-03 06:14:04.52983+00	ed504b9b-7ed0-403a-b26b-003cbbad9b36	2021-12-03 06:14:04.530807+00	2021-12-03 06:14:04.54818+00	f	\N	Mr. John Doe	doctor_test@test.com	DOCTOR	f	test address	Dhaka Division	Dhaka	1212	1913243746	profile_photo/ed504b9b-7ed0-403a-b26b-003cbbad9b36_2021_12_03_12_14_04_538321.jpeg
pbkdf2_sha256$260000$8q1ignrNFESaiWGGjpFUfD$sZcFH9D/jvYyaXuUVEb97TFZMAM+vVelz7cwfHeHe1Q=	\N	f	f	t	2021-12-03 06:15:45.886014+00	977bbe34-1fd2-435b-b1f5-bf90d363f34f	2021-12-03 06:15:45.886783+00	2021-12-03 06:15:45.915647+00	f	\N	hospital	testing_hospital@test.com	CLINIC	f	A/D road	Bamyan	Bāmyān	12333	931949030	profile_photo/977bbe34-1fd2-435b-b1f5-bf90d363f34f_2021_12_03_12_15_45_901532.jpeg
pbkdf2_sha256$260000$GAq2gl1vtSN6FMKtlWLdaG$6q3edlvQrO16MPdNJdqh5a08yrGwjzjkaRC9R399YRU=	\N	f	f	t	2021-12-03 06:23:31.129678+00	1dc9b5f7-ef76-4c5f-9986-27f8eb721295	2021-12-03 06:23:31.130533+00	2021-12-03 06:23:31.144484+00	f	\N	hospital Name	dokto_hospital@gmail.com	CLINIC	f	Address	Ghazni	Ghazni	14299	931234566	profile_photo/1dc9b5f7-ef76-4c5f-9986-27f8eb721295_2021_12_03_12_23_31_135002.jpeg
pbkdf2_sha256$260000$9q30rCNVKkHXAl9fEyfZSW$oGFS88wGqmrel3ghqy8tHQxIANtl3yg67raGX1dYQWI=	\N	f	f	t	2021-12-03 06:28:03.44363+00	7d634e50-e284-4ecd-a54d-889bd138223c	2021-12-03 06:28:03.44489+00	2021-12-03 06:28:03.469792+00	f	\N	hospital name	mail@mailerjailer.com	CLINIC	f	Address	Bamyan	Bāmyān	12444	35529292	profile_photo/7d634e50-e284-4ecd-a54d-889bd138223c_2021_12_03_12_28_03_461675.jpeg
pbkdf2_sha256$260000$EVQJQqDwLE70aFu3IP83Oe$9hzxhB3KSkTKReeEjvvRRZyDO0ux90PglvlWwKL4oIc=	\N	f	f	t	2021-12-03 06:30:21.217091+00	27911350-88bb-43ff-85c6-d0347936563e	2021-12-03 06:30:21.217985+00	2021-12-03 06:30:21.287037+00	f	\N	hospital	hospital@hospital.com	CLINIC	f	Inyo	Ghazni	Ghazni	909	9378989898	profile_photo/27911350-88bb-43ff-85c6-d0347936563e_2021_12_03_12_30_21_280866.jpeg
pbkdf2_sha256$260000$tQxeZ3Bu0QnMFA4lq9mm2a$j1wp4z3W7PUkThz38/e/A4M+xwj5V3OdC328rzwnFUM=	\N	f	f	t	2021-12-03 07:06:31.906905+00	a91af88c-fc35-46b5-8831-5e23c00abbbc	2021-12-03 07:06:31.907476+00	2021-12-03 07:06:31.916807+00	f	\N	hospital	testing_a_clinic@dokto.com	CLINIC	f	56/AD . Masdair Road	Ghazni	Ghazni	1000	9312345678	profile_photo/a91af88c-fc35-46b5-8831-5e23c00abbbc_2021_12_03_13_06_31_911447.jpeg
pbkdf2_sha256$260000$F3M6tKzsJGugGH6uWdjyXm$oriMPTKuqh/wPwXvOhWujluK5DTdvno/JIQ2PRTJKb8=	\N	f	f	t	2021-12-03 07:09:07.27956+00	69563331-2401-4acb-98e3-4089f7298f45	2021-12-03 07:09:07.280291+00	2021-12-03 07:09:07.292091+00	f	\N	pharmacy_giri	email@doktomail.com	PHARMACY	f	Address	Ghazni	Ghazni	1455	931234567	profile_photo/69563331-2401-4acb-98e3-4089f7298f45_2021_12_03_13_09_07_286480.jpeg
pbkdf2_sha256$260000$hG6Gaa7SJObRIi295Rvz5c$Cq6R3OtfXi1cGYqfxwBNmMeQJLwR7xypfB2HKfpgeoo=	\N	f	f	t	2021-12-03 08:55:37.867349+00	49dbba2e-f487-4c5c-aa4b-3964d34b6711	2021-12-03 08:55:37.868162+00	2021-12-03 08:55:37.880077+00	f	\N	Arlene Test	test2@klik4health.com	PATIENT	f	129 Main Street	New Jersey	Allentown	07012	19736789056	profile_photo/49dbba2e-f487-4c5c-aa4b-3964d34b6711_2021_12_03_14_55_37_874666.png
pbkdf2_sha256$260000$vUm9pGh99chl93q75ivLi3$Mf3MBlrJsTBoXx42EyX77vHMxykcsiLAvBp8orN6ZBw=	\N	f	f	t	2021-12-03 10:25:46.080423+00	10210419-bb1d-4192-af63-77fc3b86fa4a	2021-12-03 10:25:46.081038+00	2021-12-03 10:25:46.089289+00	f	\N	First name Last name	test@doktotest.com	PATIENT	f	test address	Bangladesh	Dhaka	1212	1913243746	profile_photo/10210419-bb1d-4192-af63-77fc3b86fa4a_2021_12_03_16_25_46_084767.jpeg
pbkdf2_sha256$260000$8NKspTExlc2bFb6yLKaOKN$wu/fit38lLCv2b/cNifpy8MIj8F/EYl1xeCgaeH9Mxk=	\N	f	f	t	2021-12-03 10:35:18.901026+00	b75bc244-cd62-4d39-b257-2820aa43eeb8	2021-12-03 10:35:18.902216+00	2021-12-03 10:35:18.912798+00	f	\N	jason  haque	jason@dokto.com	PATIENT	f	address	Dhaka District	Dhaka	1212	1913243746	profile_photo/b75bc244-cd62-4d39-b257-2820aa43eeb8_2021_12_03_16_35_18_906800.jpeg
pbkdf2_sha256$260000$oU783aCF4acIQG7MU4XMOq$M9Z9EkVOGjD9GS5lgW6DEZlvWQMfMxfuDI9EbkzTLFs=	\N	f	f	t	2021-12-03 10:37:13.293444+00	81a1c762-0527-457c-88f4-ac0dd02e870d	2021-12-03 10:37:13.294358+00	2021-12-03 10:37:13.302887+00	f	\N	Full name	saad@doktotest.com	DOCTOR	f	test address	Dhaka Division	Dhaka	1212	1913243746	profile_photo/81a1c762-0527-457c-88f4-ac0dd02e870d_2021_12_03_16_37_13_298189.jpeg
pbkdf2_sha256$260000$kHvqrGn2lOp71WfaUH9UgH$brtDy2CyiR/YZTvxfuloxGC6rzeI7uYGy4Yqa0Oczps=	\N	f	f	t	2021-12-03 10:38:30.843296+00	b8c2953f-2b6b-4407-a54c-7416f78541e9	2021-12-03 10:38:30.844057+00	2021-12-03 10:38:30.86866+00	f	\N	new clinic	hospital@hospitaltest.com	CLINIC	f	kabul road	Ghazni	Ghazni	1200	93125478	profile_photo/b8c2953f-2b6b-4407-a54c-7416f78541e9_2021_12_03_16_38_30_856755.jpeg
pbkdf2_sha256$260000$LSseYNqz3jaLFF4cYvLvVb$yIcW92mhXBNjJ2HU+1qmbrP69NNMYrqR6OJ2cOb3xBc=	\N	f	f	t	2021-12-03 13:50:06.386336+00	f7eb6b06-45b4-4b44-afd0-2544d3284303	2021-12-03 13:50:06.387139+00	2021-12-17 13:58:31.333444+00	f	\N	Klik Hospital	admin@klik4health.com	CLINIC	f	123 Main Street	Berane Municipality	Kibakwe	99545	2554048997676	profile_photo/f7eb6b06-45b4-4b44-afd0-2544d3284303_2021_12_03_19_50_06_392584.png
pbkdf2_sha256$260000$KONUSNP80nQUg7wPVuiHmB$ColIzlwovMYu/OgVSJpqZVLssODlsmyXrRXrLmnz2eE=	\N	f	f	t	2021-12-04 17:37:50.451645+00	7765be45-f16d-41a0-b1a1-24498b59eeac	2021-12-04 17:37:50.452237+00	2021-12-04 17:37:50.460032+00	f	\N	shafayat hossain	patientshafayat@gmail.com	PATIENT	f	address	Saint Mary Parish	\N	123404	+1-268124384046	profile_photo/7765be45-f16d-41a0-b1a1-24498b59eeac_2021_12_04_23_37_50_455239.jpeg
pbkdf2_sha256$260000$0WF2SQW1w8l7BbV9gN1yKt$p4beXFe/z0ENqloFeJoR2mk9x5oZQGPoM8I4FWcbieQ=	\N	f	f	t	2021-12-04 17:42:50.351859+00	5faf1dc6-fa78-4082-b4a6-8b2a00cd715d	2021-12-04 17:42:50.352386+00	2021-12-04 17:42:50.368229+00	f	\N	shafayat hossain	doctorshafayat@gmail.com	DOCTOR	f	address	Cuanza Norte Province	N’dalatando	453081	24412404648	profile_photo/5faf1dc6-fa78-4082-b4a6-8b2a00cd715d_2021_12_04_23_42_50_362035.png
pbkdf2_sha256$260000$KvGMoEXLonShpsjtEd1RSu$ZeZ4fQyuccu+hbcPv/UmkTlHD9Ayu01ZV0tk2e93d9M=	\N	f	f	t	2021-12-07 03:05:59.425628+00	c815552a-0f4b-48da-a871-f86a4ed15268	2021-12-07 03:05:59.426411+00	2021-12-07 03:05:59.437669+00	f	\N	Babul Hayat	user2@example.com	PATIENT	f	Jessore Hospital Road	Khulna	Jessore	8450	0123635237383	profile_photo/c815552a-0f4b-48da-a871-f86a4ed15268_2021_12_07_09_05_59_430623.png
pbkdf2_sha256$260000$4a8tK46gWhUsGGdhPMUko8$xipXhXbXOtfDo1839m4S+67cEE+StXVX8qwnG+ixv/M=	\N	f	f	t	2021-12-07 12:52:54.078157+00	64f65ba5-7d1d-4bfb-a54a-cb94b271e652	2021-12-07 12:52:54.079054+00	2021-12-07 12:52:54.109237+00	f	\N	Mahmudul ALam	mahmudul2@dokto.com	DOCTOR	f	string	string	string	string	string	profile_photo/64f65ba5-7d1d-4bfb-a54a-cb94b271e652_2021_12_07_18_52_54_084891.jpeg
pbkdf2_sha256$260000$0Ez1H8wFZgyu2HucQvERW3$dXAvo9qgWVxer1eKmL/gSsqkVCBS5WX5nWXAmGig/v8=	\N	f	f	t	2021-12-08 04:49:00.71115+00	89a45785-8ce9-4605-b28a-e123a7c47025	2021-12-08 04:49:00.712032+00	2021-12-08 04:49:34.435658+00	f	\N	Samnan Rahee	namanush.rsr.16@gmail.com	DOCTOR	t	236/c, vuianpara, sipahibag, khilgaon	Highland	\N	1100	880+8801521436367	profile_photo/89a45785-8ce9-4605-b28a-e123a7c47025_2021_12_08_10_49_00_717495.png
pbkdf2_sha256$260000$iiuxEhmDfUS0Y5if2YZLSC$O6YC4cqL7qyL3ygEVdlzUeJhrljfQbmvR/l6X+NNV4M=	\N	f	f	t	2021-12-08 04:58:09.811716+00	53f3d1ab-6ef4-423f-abbe-2f502d021ac0	2021-12-08 04:58:09.812435+00	2021-12-08 07:09:20.54834+00	f	\N	Samnan Rahee	info@vnsync.net	PATIENT	t	236/c, vuianpara, sipahibag, khilgaon	\N	\N	1100	88001521436367	profile_photo/53f3d1ab-6ef4-423f-abbe-2f502d021ac0_2021_12_08_10_58_09_816270.png
pbkdf2_sha256$260000$K2XxkRN93dl08Benk5TCGa$PmctXKlOtQv6IyFy84xvPN6IXT/vEWcEuohtR9YJ5kQ=	\N	f	f	t	2021-12-08 05:30:56.982746+00	3beb642d-d876-4d39-8539-8efb9def2622	2021-12-08 05:30:56.983331+00	2021-12-08 05:30:56.992216+00	f	\N	Clinic Name	clinic@dokto.com	CLINIC	f	236/c, vuianpara, sipahibag, khilgaon	Central Region	\N	1100	8801521436367	profile_photo/3beb642d-d876-4d39-8539-8efb9def2622_2021_12_08_11_30_56_987146.svgxml
pbkdf2_sha256$260000$BAVgxBfVmV0D4SF2x5ynQo$0S+4oLKrXEvXt6JdjC6epNEMtz+yUq3WJadiUieqni8=	\N	f	f	t	2021-12-08 05:35:17.539025+00	74096425-92ab-49d7-ad1a-c35b355e3260	2021-12-08 05:35:17.539733+00	2021-12-08 05:35:17.553377+00	f	\N	Samnan Rahee	test-email@dokto.com	PHARMACY	f	236/c, vuianpara, sipahibag, khilgaon	Plužine Municipality	\N	1100	8801521436367	profile_photo/74096425-92ab-49d7-ad1a-c35b355e3260_2021_12_08_11_35_17_547081.png
pbkdf2_sha256$260000$tCd9cCHZJSmrtp27Bul0qD$2JjR+Sp1GRGhn+c98khgg9upphLIj8Q69gsrig3PQgU=	\N	f	f	t	2021-12-09 10:02:08.333475+00	5d454090-2584-4953-852c-c6a0e2c2d30e	2021-12-09 10:02:08.334698+00	2021-12-17 16:56:34.841355+00	f	\N	Arlene Test	test2@dokto.com	PATIENT	t	123 Main Street	Akwa Ibom State	Bethel	99545	19736789056	profile_photo/5d454090-2584-4953-852c-c6a0e2c2d30e_2021_12_09_16_02_08_342152.png
pbkdf2_sha256$260000$lQVgZmj6zVxoPUuFdtQotm$PWw6e4zFacWUHow1uWwtAssMAHzJ8sxorlBQ7qdLEpo=	\N	f	f	t	2021-12-09 13:15:21.06877+00	fbfe7a13-6ef7-4094-b211-6407aeeb1f30	2021-12-09 13:15:21.0694+00	2021-12-23 15:46:01.75124+00	f	\N	David Test	test1@dokto.com	DOCTOR	t	123 Main Street	New Jersey	Allentown	07015	19738976754	profile_photo/fbfe7a13-6ef7-4094-b211-6407aeeb1f30_2021_12_09_19_15_21_073937.png
pbkdf2_sha256$260000$LUVQfR2cgC7HYDcqaPBmPG$mM8hIZeapVEzL4TVCxSDMBThvgz7Nj40fkLf9foQx6w=	\N	f	f	t	2021-12-10 04:42:41.493407+00	fc8297cd-9b86-4033-a97e-da5abe71d76f	2021-12-10 04:42:41.4943+00	2021-12-14 08:12:32.749281+00	f	\N	Sihan Tawsik	doctordokto@gmail.com	DOCTOR	f	32, Abul Khoyrat Road	Central Region	\N	1100	8801642518822	profile_photo/fc8297cd-9b86-4033-a97e-da5abe71d76f_2021_12_10_10_42_41_502060.jpeg
pbkdf2_sha256$260000$dFpgZK3nxPKUQsPQ4e99Bd$xyRI6u0hA4KlLqFlVhYmQvsReeehRn643xeK+tfIyyU=	\N	f	f	t	2021-12-10 04:45:22.809315+00	74df4c91-61c9-4d1f-8c5e-05fef52eecf9	2021-12-10 04:45:22.809776+00	2021-12-15 04:46:34.167269+00	f	\N	Prodipta Banarjee	probanerjee175@gmail.com	PATIENT	f	Masdair Gudaraghat	Plav Municipality	Gazipur	1400	8801521435473	profile_photo/74df4c91-61c9-4d1f-8c5e-05fef52eecf9_2021_12_10_10_45_22_813043.jpeg
pbkdf2_sha256$260000$EsEsGTTypPawjBiHzXPTex$8HHn90ZOYaA8YPUNBNF3SCxupngDaKQlZMTuby6FDLI=	\N	f	f	t	2021-12-10 14:53:01.220072+00	a0312245-e73a-4763-9a27-5a2aba93cda3	2021-12-10 14:53:01.220973+00	2021-12-10 14:53:21.443809+00	f	\N	Rachel Onamusi	rachelonamusi@gmail.com	PATIENT	t	127 Glennallen Rd	\N	\N	28115	+1-24207948320303	profile_photo/a0312245-e73a-4763-9a27-5a2aba93cda3_2021_12_10_20_53_01_229233.jpeg
pbkdf2_sha256$260000$D4Wor6hvFWca93bGKoJ6hw$KepoWp8PEtpOy8H+uMuU9M4azIkQVaL6+7ah10K2Qmo=	\N	f	f	t	2021-12-10 15:34:27.66795+00	bddc3d89-087a-4ff0-9101-58ff4633bf74	2021-12-10 15:34:27.668604+00	2021-12-17 15:57:23.787116+00	f	\N	Dokto Hospital	info@dokto.com	CLINIC	t	123 Main Street	Zarqa Governorate	Chandler	85226	19738997676	profile_photo/bddc3d89-087a-4ff0-9101-58ff4633bf74_2021_12_10_21_34_27_680814.jpeg
pbkdf2_sha256$260000$ajqeVUsVP7Typ7vZIbs5jd$V577GaO7inYdFB23rjarJdwIgVlTOWr3cAuzL7fSUAg=	\N	f	f	t	2021-12-14 08:47:24.407444+00	235a9a51-9ceb-4b55-a687-46bc634eb0fa	2021-12-14 08:47:24.408239+00	2021-12-27 07:47:20.360708+00	f	\N	meh meh	afiatamanna@gmail.com	PATIENT	f	Jhilview, Jhilpar, Pirerbaag, Mirpur-2, Dhaka	Plav Municipality	Dhaka	1216	88001764365105	profile_photo/235a9a51-9ceb-4b55-a687-46bc634eb0fa_2021_12_14_14_47_24_411989.png
pbkdf2_sha256$260000$Q52q5cJMyilJW9mvu8u5e4$2z7VnSoc5NPbyzKNwVbt5+wb7XyqSJ0l7DZeHsykDlo=	\N	f	f	t	2021-12-14 17:02:15.098828+00	70b8af3e-d59d-48e7-90e6-ded64489cf7f	2021-12-14 17:02:15.099387+00	2021-12-23 13:16:44.907375+00	f	\N	Mahmudul Alam	hospital@dokto.com	CLINIC	f	dhaka	dhaka	dhaka	1207	+8809715526246	profile_photo/70b8af3e-d59d-48e7-90e6-ded64489cf7f_2021_12_23_18_31_03_875986.webp
pbkdf2_sha256$260000$J3DoqqQNJVkYZqMHVASjln$UD6PV3Bm5+ZZzXw8hb1++sW7ZYuchL8P/VG7lQ7hP5w=	\N	f	f	t	2021-12-14 19:19:15.956511+00	db3fc55b-bd76-4ce6-9874-170ab76870ca	2021-12-14 19:19:15.957237+00	2021-12-27 06:55:15.173871+00	f	\N	Fahin Pharmacy	pharmacy@dokto.com	PHARMACY	f	Streeeet Addreeeeesssss	Ménaka Region	Vienna	0000	32asdasd	profile_photo/db3fc55b-bd76-4ce6-9874-170ab76870ca_2021_12_15_01_19_15_967467.jpeg
pbkdf2_sha256$260000$HoiZuAJZu5oHHJlnoeZI1a$86wSykZ0yCka+FcyoTUGtvDoT8xtPT36kk/AVbSH1Ko=	\N	f	f	t	2021-12-15 07:24:54.277646+00	2c32724e-8565-4a35-84d7-430b411c83be	2021-12-15 07:24:54.278154+00	2021-12-15 07:25:08.167013+00	f	\N	Sihan Tawsik	hospital@sihan.com	CLINIC	f	32, Abul Khoyrat Road	Plužine Municipality	\N	1100	88001642518822	profile_photo/2c32724e-8565-4a35-84d7-430b411c83be_2021_12_15_13_24_54_287731.jpeg
pbkdf2_sha256$260000$GbUK0M0gSGrji2HVDVcyyI$gQ04u81vsaHfCxesWp3jB2sdQcHGKw12af4/FMAkPDw=	\N	f	f	t	2021-12-15 07:30:08.072273+00	121f7441-6453-455e-ab9c-4b50a64ecf66	2021-12-15 07:30:08.072829+00	2021-12-15 07:30:25.984145+00	f	\N	Sihan Tawsik Pharmacy	pharmacy@sihan.com	PHARMACY	f	32, Abul Khoyrat Road	Central Region	\N	1100	88001642518822	profile_photo/121f7441-6453-455e-ab9c-4b50a64ecf66_2021_12_15_13_30_08_077837.jpeg
pbkdf2_sha256$260000$snNyDtnLwgYnjGb3buVXCv$6KURp49GFj6sYcLXj+i0FpN3t9djpzhvnu5cUswBMTg=	\N	f	f	t	2021-12-17 06:54:47.690634+00	03f1a586-fb3e-4480-8d04-9273bb383245	2021-12-17 06:54:47.691247+00	2021-12-17 06:54:47.702086+00	f	\N	Sihan Tawsik	sihantawsik1126@gmail.com	DOCTOR	f	32, Abul Khoyrat Road	Central Region	\N	1100	88001642518822	profile_photo/03f1a586-fb3e-4480-8d04-9273bb383245_2021_12_17_12_54_47_696233.jpeg
pbkdf2_sha256$260000$1uBobNL0mVUTGiKiOnrMyN$Ij1nxcXVS9rUQA2/C3qKrtm7hdbpfeqYUfQu4z2IJuo=	\N	f	f	t	2021-12-17 16:00:15.287099+00	1d5b7522-c466-4bec-85f4-943ee6ae16c6	2021-12-17 16:00:15.288013+00	2021-12-17 16:01:03.353571+00	f	\N	Klik Pharmacy	contact@dokto.com	PHARMACY	t	123 Main Street	Zarqa Governorate	Arizona City	85201	19738997676	profile_photo/1d5b7522-c466-4bec-85f4-943ee6ae16c6_2021_12_17_22_00_15_294339.jpeg
pbkdf2_sha256$260000$sDYjjr5sUutVEBXtrAqtYY$r1GpK2vp3m+lZfDIh+55ywQBKaUdkMnVPY7/ZtJB8/w=	\N	f	f	t	2021-12-20 08:26:14.872219+00	e7556c15-90eb-42ab-b45c-0ab6cf333068	2021-12-20 08:26:14.872818+00	2021-12-27 07:48:10.829869+00	f	\N	meh	mehm@gmail.com	CLINIC	f	Jhilview, Jhilpar, Pirerbaag, Mirpur-2, Dhaka	Dhaka District	Dhaka	1216	88001764365105	profile_photo/e7556c15-90eb-42ab-b45c-0ab6cf333068_2021_12_20_14_26_14_875738.png
pbkdf2_sha256$260000$3uqlaliH1zkWdSlYEiOoMb$Y0aq/udtCfcSqpfP1gDf2s/nz6nRneIbZRDAZEbJdEE=	\N	f	f	t	2021-12-20 22:30:41.029762+00	881eb97b-ce35-4df5-8aaf-0c688c34f00c	2021-12-20 22:30:41.030552+00	2021-12-20 22:32:07.420901+00	f	\N	Abdul Hospital and CO	sabdullateef87@gmail.com	CLINIC	f	Number 10 AgogdoSegun Odonguyan	Lagos	Ikorodu	104101	23407010112514	profile_photo/881eb97b-ce35-4df5-8aaf-0c688c34f00c_2021_12_21_04_30_41_034568.jpeg
pbkdf2_sha256$260000$sd0pKbbDWHgCNVcUt2A8Yd$fVoC1G9lcd4ye5MgJ5kS1BrYe7jll0aSb2L+AitXFAQ=	\N	f	f	t	2021-12-22 06:22:48.370633+00	7c52ea4a-efb3-4d4e-804f-e9bd2049cafa	2021-12-22 06:22:48.371263+00	2021-12-23 05:23:41.920468+00	f	\N	Oyetayo Tosin Tunde	clarenceewings247@gmail.com	PHARMACY	f	12 Ifelodun Street, Ogoluwa, Osogbo	Osun	Osogbo	230232	2349037044647	profile_photo/7c52ea4a-efb3-4d4e-804f-e9bd2049cafa_2021_12_22_12_22_48_374775.png
pbkdf2_sha256$260000$z2ciJiFMXCoh2FMZSBENiQ$voDAQLkfeZLidjinDYht/uFyfxWo2FHp6FU+leuzArY=	\N	f	f	t	2021-12-22 08:27:02.378308+00	0f219fd8-c6b7-4823-a783-b0900d6743ab	2021-12-22 08:27:02.378959+00	2021-12-22 08:27:02.388154+00	f	\N	Sanviraj Zahin Haque	mail@jmailai.com	DOCTOR	f	Masdair Gudaraghat	Dhaka	Narayanganj	1400	+358-1801521435473	profile_photo/0f219fd8-c6b7-4823-a783-b0900d6743ab_2021_12_22_14_27_02_382250.png
pbkdf2_sha256$260000$21yVvIhmrPsMQsGRgo13PH$zVbQ97sVMnXJriyIxSVpLPepaXYDlai5RvlmHr98zSA=	\N	f	f	t	2021-12-22 10:18:15.268845+00	8bf64794-80d0-4d64-bfc3-8a167f4f8960	2021-12-22 10:18:15.269298+00	2021-12-25 10:22:32.153041+00	f	\N	Oyetayo Tosin Tunde	tosinoyetayo2015@gmail.com	DOCTOR	f	12 Ifelodun Street, Ogoluwa, Osogbo	Osun	Osogbo	230232	23409037044647	profile_photo/8bf64794-80d0-4d64-bfc3-8a167f4f8960_2021_12_22_16_18_15_272405.jpeg
pbkdf2_sha256$260000$fhw0ivgp2jMZlZ4k4hPvM3$sT3jFxLaRVIEeLgCaJ12tDof/leF/vkTCvI6BVdIrSU=	\N	f	f	t	2021-12-23 05:34:35.299656+00	76d927d5-9b1d-4418-badd-a970cbf72c88	2021-12-23 05:34:35.300279+00	2021-12-23 05:39:16.950678+00	f	\N	Oyetayo Tunde	pauloyetayo2016@gmail.com	PATIENT	f	12 Ifelodun Street, Ogoluwa, Osogbo	Osun	Osogbo	230232	23409037044647	profile_photo/76d927d5-9b1d-4418-badd-a970cbf72c88_2021_12_23_11_34_35_305824.png
pbkdf2_sha256$260000$wJsgukVqsKsOXLCXgvO9nq$OKxOlmtOMSDK9TKGtZ45VFSI6ci+UtNKEn8SgWa7KeQ=	\N	f	f	t	2021-12-24 05:15:38.468157+00	444d8a39-22e2-4544-a261-0ec6fc70215c	2021-12-24 05:15:38.468676+00	2021-12-24 05:15:38.477155+00	f	\N	Sanviraj Zahin Haque	mahmudul1@dokto.com	DOCTOR	f	Shs	Dhaka	Narayanganj	1400	88001521435473	profile_photo/444d8a39-22e2-4544-a261-0ec6fc70215c_2021_12_24_11_15_38_471628.jpeg
pbkdf2_sha256$260000$ofj1mZSquuVq47GjovMbYe$svgI+rDOqWLsgUmC3YjZ8JPfQarLmSdTJ9lX/I46AP4=	\N	f	f	t	2021-12-25 10:18:44.519522+00	6c0e20bd-57f4-48e6-a2bf-75319fef2cf3	2021-12-25 10:18:44.520116+00	2021-12-25 10:23:22.140675+00	f	\N	Garba Fuad	garbafuad@gmail.com	PATIENT	f	lagos	Lagos	Ikorodu	140101	2348107530220	profile_photo/6c0e20bd-57f4-48e6-a2bf-75319fef2cf3_2021_12_25_16_18_44_523019.jpeg
pbkdf2_sha256$260000$Aa0jdPWgTXMt6Xm6m4XAF5$0wTdeyIgdBb3kikV2u2OlES7LYtFYsjhV6roW8MApN8=	\N	f	f	t	2021-12-27 07:21:13.633134+00	f23ba24b-665e-4e01-8b9a-85cda57e4ad1	2021-12-27 07:21:13.633732+00	2021-12-27 07:49:08.694239+00	f	\N	meh	mehmeh@gmail.com	PHARMACY	f	Jhilview, Jhilpar, Pirerbaag, Mirpur-2, Dhaka	Dhaka District	Dhaka	1216	88001764365105	profile_photo/f23ba24b-665e-4e01-8b9a-85cda57e4ad1_2021_12_27_13_21_13_637112.jpeg
\.


--
-- Data for Name: user_user_groups; Type: TABLE DATA; Schema: public; Owner: sihan
--

COPY public.user_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: user_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: sihan
--

COPY public.user_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: user_userip; Type: TABLE DATA; Schema: public; Owner: sihan
--

COPY public.user_userip (id, created_at, updated_at, is_deleted, deleted_at, ip_address, user_id) FROM stdin;
e38bd0d7-bda1-40b5-bd77-5cee98153473	2021-11-27 07:08:11.435142+00	2021-12-03 14:24:07.765662+00	f	\N	103.112.236.75	1dd1ffe0-2113-4c97-bcf2-abe2798bba3d
1452f29a-45a7-4666-85ff-4e6bab9e6c03	2021-11-27 07:08:54.644699+00	2021-12-04 11:36:33.778392+00	f	\N	103.125.29.32	09a95982-a373-4555-9347-b963628701ac
5e4d0e49-9667-498d-a488-0cb320cad940	2021-11-27 07:10:36.480401+00	2021-12-01 07:34:38.707574+00	f	\N	103.112.236.75	09a95982-a373-4555-9347-b963628701ac
acc38971-1f88-4746-bf2e-d8b15fbc5183	2021-11-27 07:30:29.397451+00	2021-11-27 08:18:40.653224+00	f	\N	116.58.201.26	09a95982-a373-4555-9347-b963628701ac
25c6c77a-9c42-47f8-9f57-d0125587a9b6	2021-11-27 09:51:38.809694+00	2021-11-27 09:56:34.656039+00	f	\N	37.111.198.5	09a95982-a373-4555-9347-b963628701ac
d5bf6ae8-ee41-4cf7-8d1f-c467bad334d2	2021-11-27 10:04:49.368664+00	2021-11-27 10:11:51.092339+00	f	\N	103.134.255.115	2a2c60f1-e068-47d2-be66-88bd52116d20
47cd48e2-cabf-43c0-aa90-52c44557f343	2021-11-28 02:25:10.393235+00	2021-12-11 12:02:25.480601+00	f	\N	103.120.39.37	952478f7-4c6e-497a-b6c0-7f11ca93ae12
0d500a37-26e4-491b-b225-e3a18a767ddc	2021-11-28 11:35:20.968687+00	2021-12-04 11:46:50.755869+00	f	\N	59.152.111.171	1dd1ffe0-2113-4c97-bcf2-abe2798bba3d
d343c0b3-761b-42a5-9e0c-4a84bfbcab6a	2021-11-29 00:49:07.999287+00	2021-11-29 01:19:55.132628+00	f	\N	103.112.237.43	1dd1ffe0-2113-4c97-bcf2-abe2798bba3d
7baeb4b9-6839-408c-a6d9-a1d0632e11ea	2021-11-29 11:20:55.663293+00	2021-11-29 12:15:08.743446+00	f	\N	37.111.212.8	1dd1ffe0-2113-4c97-bcf2-abe2798bba3d
fd5bdda6-757f-49fa-b8d9-0bd2eb513886	2021-11-30 03:36:11.998292+00	2021-11-30 05:41:34.228059+00	f	\N	37.111.216.217	3a0edd9f-747f-4c4d-b271-bc6b38696fe4
abfb37f8-a6b2-4ff2-b579-65c4412bf213	2021-11-30 07:22:01.173842+00	2021-11-30 07:22:01.173887+00	f	\N	202.134.14.155	3a0edd9f-747f-4c4d-b271-bc6b38696fe4
06264e7b-03e4-4ba3-9066-188e1a3dc6eb	2021-11-30 11:24:33.433888+00	2021-12-03 01:26:47.072073+00	f	\N	45.127.48.27	3a0edd9f-747f-4c4d-b271-bc6b38696fe4
314c9c36-9999-47cd-a244-ad2280765fb1	2021-11-30 11:34:08.285407+00	2021-11-30 12:35:37.781062+00	f	\N	37.111.210.30	1dd1ffe0-2113-4c97-bcf2-abe2798bba3d
0a15a69a-efc0-4206-ab98-275428679657	2021-12-01 11:20:29.306219+00	2021-12-01 12:42:15.270125+00	f	\N	37.111.210.226	1dd1ffe0-2113-4c97-bcf2-abe2798bba3d
9187b5f7-d205-4895-83e9-fe2c0c1aa430	2021-12-01 13:44:32.381159+00	2021-12-07 12:02:56.153006+00	f	\N	59.152.111.169	1dd1ffe0-2113-4c97-bcf2-abe2798bba3d
c2451cc9-56a5-4399-bc25-0f42e45d8de8	2021-12-02 01:20:32.30952+00	2021-12-02 04:28:08.11776+00	f	\N	103.125.29.32	91d1b59d-b202-486a-bfcc-d9c0490a88f7
45d1b48f-189d-4e0f-b42b-fc6700262c07	2021-12-02 04:42:56.802104+00	2021-12-02 04:42:56.802162+00	f	\N	103.125.29.32	b800d6d5-deb5-4e73-806a-1a85070662f2
1eed71e1-1c24-49bb-81dd-74655ad7fbe3	2021-12-02 04:50:23.455323+00	2021-12-06 04:45:57.517746+00	f	\N	59.152.111.170	1dd1ffe0-2113-4c97-bcf2-abe2798bba3d
52ce8a62-f382-4562-a414-4f065c74ad50	2021-12-02 05:30:38.924672+00	2021-12-02 13:39:54.330328+00	f	\N	103.67.158.183	09a95982-a373-4555-9347-b963628701ac
79df1a10-0915-43ee-8e08-f4c60c170b52	2021-12-02 09:12:38.595229+00	2021-12-14 05:24:16.253371+00	f	\N	92.28.168.26	952478f7-4c6e-497a-b6c0-7f11ca93ae12
3a8b0fb0-547b-4c9b-bebf-320b7d9b2384	2021-12-03 00:59:16.040326+00	2021-12-16 06:43:38.238003+00	f	\N	103.221.55.50	952478f7-4c6e-497a-b6c0-7f11ca93ae12
f0400051-e026-45f3-be84-42668c014274	2021-12-03 02:00:24.5834+00	2021-12-03 02:06:51.794084+00	f	\N	37.111.219.213	3a0edd9f-747f-4c4d-b271-bc6b38696fe4
40b86f6d-6c7d-4a1e-b3c2-51f570256d00	2021-12-03 02:38:57.939937+00	2021-12-03 04:27:12.17919+00	f	\N	103.137.67.198	3a0edd9f-747f-4c4d-b271-bc6b38696fe4
ac63e069-d41f-46a5-848c-3e81c6814b80	2021-12-03 04:29:27.801014+00	2021-12-23 09:07:03.061639+00	f	\N	103.137.67.198	1dd1ffe0-2113-4c97-bcf2-abe2798bba3d
f6c4d538-b3ff-4b46-b58f-d0c86d88b110	2021-12-03 09:09:35.705307+00	2021-12-03 09:10:32.674749+00	f	\N	70.163.229.56	49dbba2e-f487-4c5c-aa4b-3964d34b6711
39e71eac-c8b7-4aee-92a1-076fe78289d9	2021-12-03 09:20:55.020774+00	2021-12-03 09:21:08.18151+00	f	\N	70.163.229.56	ed76b722-e7f8-46cd-8dff-f4f687856bf3
25895d5d-988e-451c-a758-66fde4c2cd8e	2021-12-03 09:53:26.539116+00	2021-12-03 15:16:32.208958+00	f	\N	70.163.229.56	952478f7-4c6e-497a-b6c0-7f11ca93ae12
7f6c25c2-b935-42d0-8a96-95a2b749c78a	2021-12-03 11:47:22.555337+00	2021-12-03 11:48:11.353915+00	f	\N	103.134.255.115	ed76b722-e7f8-46cd-8dff-f4f687856bf3
82ce8b14-3499-467e-89d1-7057c1d6c489	2021-12-03 11:48:56.6857+00	2021-12-03 12:33:51.084554+00	f	\N	59.152.111.171	09a95982-a373-4555-9347-b963628701ac
06ddebe9-a35f-467f-a0ef-a6a9ae2a01ea	2021-12-03 13:56:19.62728+00	2021-12-03 13:56:21.477906+00	f	\N	37.111.212.92	1dd1ffe0-2113-4c97-bcf2-abe2798bba3d
67799f27-61f1-4d07-b15b-529451d787b8	2021-12-03 17:16:52.028256+00	2021-12-03 17:16:58.067087+00	f	\N	96.242.93.74	952478f7-4c6e-497a-b6c0-7f11ca93ae12
6f44480d-9491-43ee-9fc2-4a37b3fff8b3	2021-12-04 08:24:23.043058+00	2021-12-04 13:10:39.147999+00	f	\N	103.112.236.78	1dd1ffe0-2113-4c97-bcf2-abe2798bba3d
b8740903-3c9d-4e7e-a5b3-456506e2d5a5	2021-12-04 09:25:05.657235+00	2021-12-04 14:09:52.220816+00	f	\N	103.134.255.115	952478f7-4c6e-497a-b6c0-7f11ca93ae12
3adf75ec-5163-454c-8d7d-cc2bcab0983e	2021-12-04 09:38:13.986871+00	2021-12-05 11:25:51.905313+00	f	\N	103.134.255.118	952478f7-4c6e-497a-b6c0-7f11ca93ae12
ab0d8d10-156a-4503-9789-5e1e5c293831	2021-12-04 11:34:00.452451+00	2021-12-04 11:57:10.186192+00	f	\N	37.111.207.25	1dd1ffe0-2113-4c97-bcf2-abe2798bba3d
009cf3f3-d08d-4179-89ea-ca67e14da524	2021-12-04 23:19:14.328201+00	2021-12-05 04:27:47.96475+00	f	\N	103.112.236.77	1dd1ffe0-2113-4c97-bcf2-abe2798bba3d
630c8fc1-4917-467c-bbb1-22f70cc4beb7	2021-12-05 07:56:11.841696+00	2021-12-05 08:36:52.054887+00	f	\N	37.111.200.211	1dd1ffe0-2113-4c97-bcf2-abe2798bba3d
bbccfbeb-f48c-401b-95a3-799a3d8a2a1a	2021-12-06 04:07:07.571491+00	2021-12-06 05:20:57.705732+00	f	\N	37.111.200.126	1dd1ffe0-2113-4c97-bcf2-abe2798bba3d
cf134044-ad97-40d1-b2c4-0638b8e2cb05	2021-12-06 05:25:46.461822+00	2021-12-06 05:39:58.259551+00	f	\N	37.111.200.126	09a95982-a373-4555-9347-b963628701ac
f21026b2-c0c2-43c9-81fc-5cba0165f2b6	2021-12-06 05:46:23.575464+00	2021-12-06 05:49:28.815636+00	f	\N	37.111.213.206	09a95982-a373-4555-9347-b963628701ac
194a5fd6-5762-434b-bf26-6fdb10b12187	2021-12-07 02:20:50.222983+00	2021-12-07 02:25:00.114352+00	f	\N	103.95.98.97	952478f7-4c6e-497a-b6c0-7f11ca93ae12
6842b8c4-2809-4dae-a30d-563260486c5a	2021-12-07 09:10:45.893385+00	2021-12-23 08:15:49.948256+00	f	\N	103.125.29.41	09a95982-a373-4555-9347-b963628701ac
b37c40b8-9944-4f43-bd6f-f4c343e969ff	2021-12-07 10:22:33.655016+00	2021-12-07 12:38:27.01078+00	f	\N	103.67.158.231	09a95982-a373-4555-9347-b963628701ac
1131d31b-9a55-4823-858d-bb00e990480a	2021-12-07 10:26:22.517314+00	2021-12-15 10:07:54.928765+00	f	\N	103.134.255.116	952478f7-4c6e-497a-b6c0-7f11ca93ae12
f408c3d6-88c5-410a-9884-3885e709c6f7	2021-12-07 11:09:18.189119+00	2021-12-08 01:21:14.380452+00	f	\N	103.112.236.77	09a95982-a373-4555-9347-b963628701ac
265c547c-abb9-4eb4-a15a-8583b0afcec5	2021-12-07 12:53:20.603459+00	2021-12-07 12:53:39.329584+00	f	\N	103.221.55.50	876b4dde-d1f6-4e79-a513-b7375b2b954c
4f6834a4-8f88-4fbd-a753-086a569d0f89	2021-12-07 13:29:56.065632+00	2021-12-10 04:05:23.435366+00	f	\N	103.134.255.116	3a0edd9f-747f-4c4d-b271-bc6b38696fe4
c60f00c6-f66c-428d-acfa-f5e76665f677	2021-12-07 23:16:49.076978+00	2021-12-07 23:49:34.771973+00	f	\N	103.95.98.97	ed76b722-e7f8-46cd-8dff-f4f687856bf3
94353a1a-b4cf-42fd-a07d-4f4191412063	2021-12-07 23:33:02.931269+00	2021-12-08 02:53:43.004645+00	f	\N	103.95.98.97	876b4dde-d1f6-4e79-a513-b7375b2b954c
ad4004cc-4f0d-4e53-bddd-a6907add45dc	2021-12-08 01:29:07.815269+00	2021-12-08 06:53:40.475592+00	f	\N	103.112.236.77	952478f7-4c6e-497a-b6c0-7f11ca93ae12
70ad2c4f-296f-4e5f-a073-dbb5798006dc	2021-12-08 03:30:08.890216+00	2021-12-13 19:19:35.696548+00	f	\N	59.152.111.169	952478f7-4c6e-497a-b6c0-7f11ca93ae12
a1132586-1599-4c7d-afa7-ab50018a279a	2021-12-08 04:59:45.081324+00	2021-12-08 04:59:45.651764+00	f	\N	59.152.111.169	53f3d1ab-6ef4-423f-abbe-2f502d021ac0
6049b049-3960-44c5-a369-e88fb0530d59	2021-12-08 05:46:46.777725+00	2021-12-08 05:47:37.563932+00	f	\N	59.152.111.169	74096425-92ab-49d7-ad1a-c35b355e3260
2f50b48c-e0ff-4f3f-94dd-d9aab4c3b95d	2021-12-08 07:14:17.869491+00	2021-12-11 09:06:28.815604+00	f	\N	103.112.236.71	952478f7-4c6e-497a-b6c0-7f11ca93ae12
8a9b43c2-8546-4ca0-9a41-6f19ad195f57	2021-12-08 08:38:25.743759+00	2021-12-13 13:05:18.71325+00	f	\N	103.120.39.37	876b4dde-d1f6-4e79-a513-b7375b2b954c
13bcd6d4-87e1-4c96-a0b2-eaac10d4c1a5	2021-12-09 08:02:37.974675+00	2021-12-09 08:03:58.230661+00	f	\N	37.111.195.164	952478f7-4c6e-497a-b6c0-7f11ca93ae12
614be6b6-e889-4c17-9e4d-ea91bdb285d0	2021-12-09 08:50:18.397542+00	2021-12-27 07:42:31.478846+00	f	\N	103.125.29.41	952478f7-4c6e-497a-b6c0-7f11ca93ae12
8f4aacde-fa86-4190-b9a2-b5456456a6d7	2021-12-09 09:54:19.44269+00	2021-12-11 15:14:12.208569+00	f	\N	92.28.168.26	ed76b722-e7f8-46cd-8dff-f4f687856bf3
24a7acf2-d363-462f-9ffa-5808ce2709a1	2021-12-09 10:04:27.559558+00	2021-12-11 09:19:48.808365+00	f	\N	103.134.255.116	876b4dde-d1f6-4e79-a513-b7375b2b954c
78ca3477-85e6-476f-9ae5-271dd95e56ee	2021-12-09 11:49:33.774904+00	2021-12-09 11:51:32.775024+00	f	\N	103.67.158.231	952478f7-4c6e-497a-b6c0-7f11ca93ae12
ecec2c9b-f5fd-4bb3-919b-f91a0c1fb0d9	2021-12-09 12:37:06.856463+00	2021-12-17 17:30:40.97259+00	f	\N	70.163.229.56	5d454090-2584-4953-852c-c6a0e2c2d30e
6fa6f21e-5c7d-4a45-8861-2b6ad7979265	2021-12-09 13:16:10.374135+00	2021-12-17 16:59:09.809366+00	f	\N	70.163.229.56	fbfe7a13-6ef7-4094-b211-6407aeeb1f30
27a43dfd-5ff7-40b0-a538-3f07415ade7d	2021-12-10 03:29:02.220779+00	2021-12-10 04:22:08.419474+00	f	\N	37.111.199.213	876b4dde-d1f6-4e79-a513-b7375b2b954c
c5f37fc0-b668-460d-83c2-f113009dd7ae	2021-12-10 04:03:02.69068+00	2021-12-10 04:04:12.555824+00	f	\N	37.111.199.213	952478f7-4c6e-497a-b6c0-7f11ca93ae12
42180fb9-a87e-44d6-a795-300db110b238	2021-12-10 04:22:51.922802+00	2021-12-10 04:41:47.328848+00	f	\N	37.111.200.187	876b4dde-d1f6-4e79-a513-b7375b2b954c
e64b3900-54df-417f-89f8-25a2e661637f	2021-12-10 04:48:49.868208+00	2021-12-10 07:40:59.038196+00	f	\N	103.137.67.198	74df4c91-61c9-4d1f-8c5e-05fef52eecf9
ad83f367-e64a-4f51-901c-9d1f01351dc7	2021-12-10 05:59:31.911437+00	2021-12-14 08:17:14.526949+00	f	\N	103.125.29.41	fc8297cd-9b86-4033-a97e-da5abe71d76f
702ddf81-8d69-4628-826a-2d64c8e5bf7d	2021-12-10 08:28:24.465776+00	2021-12-10 08:54:54.459974+00	f	\N	37.111.196.78	952478f7-4c6e-497a-b6c0-7f11ca93ae12
5340c128-ff0f-4acc-985b-9d1f785e3a77	2021-12-10 08:38:34.772598+00	2021-12-10 08:39:12.64264+00	f	\N	103.67.158.231	fc8297cd-9b86-4033-a97e-da5abe71d76f
1e35e4f5-7407-43f6-96cf-2229cabb22c6	2021-12-10 09:20:12.882458+00	2021-12-21 18:42:37.835857+00	f	\N	59.152.111.170	952478f7-4c6e-497a-b6c0-7f11ca93ae12
47f2460c-84a9-49bf-a9f4-d3f06e18c404	2021-12-10 13:00:54.919078+00	2021-12-23 12:58:24.411401+00	f	\N	103.125.29.41	876b4dde-d1f6-4e79-a513-b7375b2b954c
91b3806b-db22-4d4e-b0df-a50d83ff2967	2021-12-10 14:54:22.069926+00	2021-12-10 14:56:49.127228+00	f	\N	92.28.168.26	a0312245-e73a-4763-9a27-5a2aba93cda3
d193e62d-194a-4836-93bb-c508c9a5213b	2021-12-10 15:35:49.690854+00	2021-12-10 15:36:03.103517+00	f	\N	70.163.229.56	bddc3d89-087a-4ff0-9101-58ff4633bf74
5077f31a-178f-4fdb-bd4b-ba857b53e62e	2021-12-10 17:02:50.686536+00	2021-12-10 17:11:16.171054+00	f	\N	197.210.70.138	ed76b722-e7f8-46cd-8dff-f4f687856bf3
bfe9e9ba-e217-45a8-a9e6-3f91e463e526	2021-12-10 17:03:07.650301+00	2021-12-10 17:04:36.258145+00	f	\N	102.91.5.171	ed76b722-e7f8-46cd-8dff-f4f687856bf3
3e9c9a12-0504-46ba-ae75-dbf85954e892	2021-12-10 17:20:31.276906+00	2021-12-10 17:20:31.276946+00	f	\N	197.210.70.54	ed76b722-e7f8-46cd-8dff-f4f687856bf3
49f595ad-08c3-4881-9f68-a5fff1cf4c12	2021-12-10 17:22:54.274361+00	2021-12-10 17:29:00.252728+00	f	\N	197.210.70.54	fbfe7a13-6ef7-4094-b211-6407aeeb1f30
91cb29eb-324a-476d-894b-3f1cf1b5fe46	2021-12-10 17:26:37.640613+00	2021-12-10 17:26:37.640653+00	f	\N	102.91.5.171	fbfe7a13-6ef7-4094-b211-6407aeeb1f30
b230e79f-b234-43fd-b8b9-6f360c2d1e3e	2021-12-11 02:31:35.201325+00	2021-12-11 02:34:51.887856+00	f	\N	103.67.157.78	876b4dde-d1f6-4e79-a513-b7375b2b954c
fc681740-2c3d-4f1d-838c-05307d24c7de	2021-12-11 04:54:24.659252+00	2021-12-14 09:58:26.828017+00	f	\N	103.67.157.78	fc8297cd-9b86-4033-a97e-da5abe71d76f
dd7ad4cd-0b79-4146-883b-cdb9c9054f04	2021-12-11 07:34:28.032921+00	2021-12-11 07:35:18.587711+00	f	\N	103.134.255.116	09a95982-a373-4555-9347-b963628701ac
458d7416-5509-466c-b749-779b3948f1ca	2021-12-11 08:43:42.945506+00	2021-12-16 06:40:51.471982+00	f	\N	103.221.55.50	ed76b722-e7f8-46cd-8dff-f4f687856bf3
dded21b6-676e-4de1-a5d9-9f2c792d874c	2021-12-11 09:02:16.2141+00	2021-12-11 09:31:25.07845+00	f	\N	103.120.39.37	ed76b722-e7f8-46cd-8dff-f4f687856bf3
c453dc00-9112-4b27-895a-e739dca616b8	2021-12-11 09:47:48.136951+00	2021-12-11 09:47:48.136983+00	f	\N	138.199.28.51	fbfe7a13-6ef7-4094-b211-6407aeeb1f30
505815fd-7175-42dd-b34d-bfedab370e10	2021-12-11 15:24:15.860218+00	2021-12-11 15:24:15.960585+00	f	\N	108.58.172.53	fbfe7a13-6ef7-4094-b211-6407aeeb1f30
d1b8756b-34d7-401b-b14e-570650a86dfd	2021-12-11 15:33:25.388018+00	2021-12-11 15:37:33.264087+00	f	\N	108.58.172.53	5d454090-2584-4953-852c-c6a0e2c2d30e
1e04b87f-cd86-4692-8fe3-8a2bffe9b1cd	2021-12-12 01:16:08.600573+00	2021-12-12 08:53:05.594224+00	f	\N	103.112.236.65	952478f7-4c6e-497a-b6c0-7f11ca93ae12
03fc6044-0f3c-4668-9f79-a5e9299f53ab	2021-12-12 07:56:01.508703+00	2021-12-12 08:21:24.807501+00	f	\N	202.134.8.136	1dd1ffe0-2113-4c97-bcf2-abe2798bba3d
856b7a4d-bf82-4ef1-ac49-857ba6efdd2c	2021-12-12 11:56:56.287736+00	2021-12-22 08:59:16.697667+00	f	\N	45.127.48.204	1dd1ffe0-2113-4c97-bcf2-abe2798bba3d
b327ff41-ef10-4c82-bb06-1734f9cd946c	2021-12-12 22:16:36.717928+00	2021-12-12 22:17:05.841156+00	f	\N	37.111.211.115	952478f7-4c6e-497a-b6c0-7f11ca93ae12
bab4ea60-5b31-4be8-a8b1-6a4c35cbc3fb	2021-12-13 22:33:38.360411+00	2021-12-13 22:40:15.690105+00	f	\N	103.112.236.79	952478f7-4c6e-497a-b6c0-7f11ca93ae12
6b136895-3c1c-4463-b8cf-787ae91a5db2	2021-12-14 08:49:25.747418+00	2021-12-14 12:22:45.75417+00	f	\N	103.112.236.79	235a9a51-9ceb-4b55-a687-46bc634eb0fa
646c0aca-72ee-4802-a29c-354eb44a5a2a	2021-12-14 10:05:11.811228+00	2021-12-14 10:05:46.620986+00	f	\N	103.67.157.78	952478f7-4c6e-497a-b6c0-7f11ca93ae12
486b7730-97e2-4bb6-816f-912fd40e1187	2021-12-14 10:54:31.073364+00	2021-12-16 12:58:13.828988+00	f	\N	39.41.7.25	952478f7-4c6e-497a-b6c0-7f11ca93ae12
d59e6f07-0269-4952-88e3-3837e24622e6	2021-12-14 20:25:33.854509+00	2021-12-23 12:46:45.811727+00	f	\N	59.152.111.168	876b4dde-d1f6-4e79-a513-b7375b2b954c
51ca70b2-7ff5-4b23-820f-4249e52c38ba	2021-12-14 20:25:53.926614+00	2021-12-23 10:31:16.12342+00	f	\N	59.152.111.168	952478f7-4c6e-497a-b6c0-7f11ca93ae12
b59b0e37-70ce-4246-908a-769e9fb934d8	2021-12-14 21:10:19.848413+00	2021-12-14 21:17:06.499117+00	f	\N	202.69.61.210	952478f7-4c6e-497a-b6c0-7f11ca93ae12
bbd2b466-4533-4a64-bb68-8460ca9b16b8	2021-12-14 21:15:21.383983+00	2021-12-14 21:16:46.845125+00	f	\N	156.146.59.45	952478f7-4c6e-497a-b6c0-7f11ca93ae12
4ac55b46-701b-4618-bfb9-874b0565ba47	2021-12-15 04:38:04.998005+00	2021-12-15 04:38:15.184531+00	f	\N	103.23.40.103	db3fc55b-bd76-4ce6-9874-170ab76870ca
8f913178-5e48-4900-ab57-4b0bde24d7d1	2021-12-15 04:39:51.10078+00	2021-12-15 04:39:51.847467+00	f	\N	103.23.40.103	70b8af3e-d59d-48e7-90e6-ded64489cf7f
f0a08eb1-0067-444b-b6ee-bcd3ed2ba15e	2021-12-15 04:46:42.33019+00	2021-12-15 04:52:08.828602+00	f	\N	103.23.40.103	74df4c91-61c9-4d1f-8c5e-05fef52eecf9
f343e8f0-f0d1-4b57-a406-82fc842e0bb1	2021-12-15 05:00:34.534243+00	2021-12-16 02:30:23.052748+00	f	\N	103.120.36.108	876b4dde-d1f6-4e79-a513-b7375b2b954c
a06d806a-1775-4038-8588-cb6a1d7b6281	2021-12-15 05:43:27.838404+00	2021-12-16 00:59:31.828725+00	f	\N	103.120.36.108	952478f7-4c6e-497a-b6c0-7f11ca93ae12
af02832f-317f-43fd-beda-bb7a351cf6e2	2021-12-15 08:10:02.943475+00	2021-12-15 08:10:05.437166+00	f	\N	37.111.202.245	235a9a51-9ceb-4b55-a687-46bc634eb0fa
32f56cf8-531c-4741-8ede-7bce6eb1e071	2021-12-15 08:44:19.283937+00	2021-12-15 08:44:39.054195+00	f	\N	59.152.111.170	70b8af3e-d59d-48e7-90e6-ded64489cf7f
cc5722d2-8dfb-46af-9d75-612cab1799d7	2021-12-15 10:39:03.870661+00	2021-12-22 05:45:19.005931+00	f	\N	92.28.179.54	952478f7-4c6e-497a-b6c0-7f11ca93ae12
fe5d89f8-1716-4391-b918-a598e48090c2	2021-12-15 11:21:17.042044+00	2021-12-21 11:46:36.420516+00	f	\N	92.28.179.54	ed76b722-e7f8-46cd-8dff-f4f687856bf3
e01a679e-cd01-443d-aec3-3a5d3cef634b	2021-12-15 15:54:53.65329+00	2021-12-19 20:19:00.633997+00	f	\N	59.152.111.171	952478f7-4c6e-497a-b6c0-7f11ca93ae12
59b814ce-c560-4e7c-b024-bffa85419e8d	2021-12-15 18:00:51.571359+00	2021-12-15 18:01:25.81655+00	f	\N	59.152.111.171	876b4dde-d1f6-4e79-a513-b7375b2b954c
2db58830-8e87-4d87-a530-1accf4dada84	2021-12-16 09:20:52.851354+00	2021-12-20 09:39:32.001128+00	f	\N	103.120.38.200	876b4dde-d1f6-4e79-a513-b7375b2b954c
3d637eaf-8016-42d9-b89a-44f628f62957	2021-12-16 10:11:03.538844+00	2021-12-23 10:20:28.880309+00	f	\N	103.120.38.200	952478f7-4c6e-497a-b6c0-7f11ca93ae12
9ccb59c0-b865-4316-ab37-9280a14eea66	2021-12-16 10:11:55.237108+00	2021-12-16 10:11:55.237163+00	f	\N	103.67.158.168	952478f7-4c6e-497a-b6c0-7f11ca93ae12
45936fd3-630b-4fd2-819e-cdeeb2dd280d	2021-12-16 12:31:15.101632+00	2021-12-17 09:44:10.195016+00	f	\N	103.67.158.168	876b4dde-d1f6-4e79-a513-b7375b2b954c
8f8169b1-1e16-47bb-81ad-8356e6c27235	2021-12-17 03:27:20.322815+00	2021-12-17 07:58:10.78887+00	f	\N	39.41.120.15	952478f7-4c6e-497a-b6c0-7f11ca93ae12
0e1d7ffa-c8f6-43e4-87a4-59d3d27b6df1	2021-12-17 12:32:38.395835+00	2021-12-17 12:33:32.185303+00	f	\N	103.134.255.117	876b4dde-d1f6-4e79-a513-b7375b2b954c
10b6ce5a-5f6a-4a54-8dc3-8800934cdda3	2021-12-17 14:09:35.937773+00	2021-12-17 14:09:55.589592+00	f	\N	70.163.229.56	f7eb6b06-45b4-4b44-afd0-2544d3284303
b4e31df3-593c-42e8-b854-bf75fb5f2f5d	2021-12-17 16:01:21.649116+00	2021-12-17 16:01:21.649161+00	f	\N	70.163.229.56	1d5b7522-c466-4bec-85f4-943ee6ae16c6
82b654d5-6a2a-4a3b-af54-a17b62429e34	2021-12-18 03:37:42.332058+00	2021-12-18 03:37:42.332113+00	f	\N	37.111.206.208	235a9a51-9ceb-4b55-a687-46bc634eb0fa
e5c5e959-49c9-4113-b865-51c19c62f44c	2021-12-18 09:40:27.605866+00	2021-12-18 09:40:27.605902+00	f	\N	37.111.196.228	235a9a51-9ceb-4b55-a687-46bc634eb0fa
fa099343-c581-4d37-9271-63f41467b325	2021-12-19 01:07:32.51841+00	2021-12-19 01:07:37.748861+00	f	\N	103.166.25.4	235a9a51-9ceb-4b55-a687-46bc634eb0fa
aaec18c2-a495-4c4c-ae6a-c059574c4956	2021-12-19 08:19:32.824166+00	2021-12-19 08:23:09.688813+00	f	\N	37.111.199.11	09a95982-a373-4555-9347-b963628701ac
2f689e14-22b0-456b-a302-af77b8931041	2021-12-19 09:00:35.459932+00	2021-12-19 09:00:36.228467+00	f	\N	37.111.199.11	952478f7-4c6e-497a-b6c0-7f11ca93ae12
bb6c4c3b-130b-4998-b7cb-8fa9cf7ef27d	2021-12-20 00:21:02.88588+00	2021-12-22 12:23:55.144757+00	f	\N	103.67.158.24	952478f7-4c6e-497a-b6c0-7f11ca93ae12
f3975d8c-24fd-4709-97f4-0a1ff527d1d4	2021-12-20 08:01:16.954932+00	2021-12-22 12:32:49.072622+00	f	\N	103.67.158.24	876b4dde-d1f6-4e79-a513-b7375b2b954c
ca1d3564-f8fc-4dd1-a2f2-13a103414756	2021-12-20 08:27:11.890421+00	2021-12-20 09:12:37.392872+00	f	\N	103.166.25.4	e7556c15-90eb-42ab-b45c-0ab6cf333068
08c0260f-b783-430f-b63d-f019c24ac916	2021-12-20 12:45:27.34511+00	2021-12-20 12:46:25.189777+00	f	\N	103.134.255.117	fc8297cd-9b86-4033-a97e-da5abe71d76f
53838027-bd86-4505-8a1d-296249ce324f	2021-12-20 12:47:42.560933+00	2021-12-20 12:50:19.206013+00	f	\N	103.134.255.117	952478f7-4c6e-497a-b6c0-7f11ca93ae12
103a1df7-81b8-4524-acb7-ad8c5825fcd8	2021-12-20 12:55:06.041082+00	2021-12-20 12:59:25.644809+00	f	\N	103.134.255.117	3a0edd9f-747f-4c4d-b271-bc6b38696fe4
bc6193ce-f089-431a-916f-c7c5c715cf95	2021-12-20 13:02:34.653365+00	2021-12-20 13:18:08.674801+00	f	\N	103.134.255.117	09a95982-a373-4555-9347-b963628701ac
92321ce4-51bf-4165-9bf7-091694a33558	2021-12-22 04:09:31.288971+00	2021-12-27 07:26:12.616969+00	f	\N	103.134.255.114	952478f7-4c6e-497a-b6c0-7f11ca93ae12
79217239-d143-4c91-8a9e-c2fddc00d02a	2021-12-22 09:04:30.77472+00	2021-12-22 09:04:30.774756+00	f	\N	37.111.210.83	e7556c15-90eb-42ab-b45c-0ab6cf333068
d3be2952-6fa6-4aa1-834e-dda8fd5568be	2021-12-22 10:19:09.47356+00	2021-12-22 14:19:43.46345+00	f	\N	197.210.28.28	8bf64794-80d0-4d64-bfc3-8a167f4f8960
5b8ad177-c501-4e72-b13c-4518900b4e2a	2021-12-22 14:39:39.441985+00	2021-12-22 15:38:18.128508+00	f	\N	197.210.55.161	8bf64794-80d0-4d64-bfc3-8a167f4f8960
7eec3838-efdb-4510-bcf1-2dc437bf828d	2021-12-22 14:55:19.169521+00	2021-12-22 16:11:10.646144+00	f	\N	197.210.226.153	8bf64794-80d0-4d64-bfc3-8a167f4f8960
44f40744-d63c-45f6-a760-5d470cc42c2b	2021-12-22 15:29:52.544121+00	2021-12-22 16:23:32.328827+00	f	\N	197.210.54.25	8bf64794-80d0-4d64-bfc3-8a167f4f8960
3bb7e829-b019-40bb-88e5-5bb5947a488c	2021-12-23 01:06:09.02071+00	2021-12-23 01:06:55.732414+00	f	\N	103.67.158.16	952478f7-4c6e-497a-b6c0-7f11ca93ae12
33aa858a-0de3-4425-b64a-22462c11e484	2021-12-23 01:30:55.907222+00	2021-12-23 12:23:19.983993+00	f	\N	103.134.255.114	876b4dde-d1f6-4e79-a513-b7375b2b954c
0a54c7a4-dc2f-498f-9407-935db6d135ce	2021-12-23 02:39:00.846074+00	2021-12-23 02:39:00.84611+00	f	\N	37.111.205.228	235a9a51-9ceb-4b55-a687-46bc634eb0fa
8c127cf1-c547-4d19-be75-62012b36f18b	2021-12-23 04:09:57.57629+00	2021-12-23 07:28:09.663434+00	f	\N	197.211.32.226	8bf64794-80d0-4d64-bfc3-8a167f4f8960
99c77585-e4ed-41ba-9679-5cebaa0f384d	2021-12-23 05:23:48.635872+00	2021-12-23 05:23:48.635925+00	f	\N	197.211.32.226	7c52ea4a-efb3-4d4e-804f-e9bd2049cafa
de060f2e-a9f7-421a-b08f-390faa51d1ab	2021-12-23 05:35:06.466744+00	2021-12-23 05:35:06.466782+00	f	\N	197.211.32.226	76d927d5-9b1d-4418-badd-a970cbf72c88
99aab453-9765-400e-8ef0-144e96b3e367	2021-12-23 09:51:29.828204+00	2021-12-23 10:02:04.735044+00	f	\N	103.221.55.50	2a2c60f1-e068-47d2-be66-88bd52116d20
04f67f68-7184-4bba-889f-32c5447f460e	2021-12-23 09:59:06.045112+00	2021-12-23 14:43:13.800192+00	f	\N	102.89.0.165	8bf64794-80d0-4d64-bfc3-8a167f4f8960
89a3b712-8a31-479e-9481-3fcc0ab17418	2021-12-23 10:04:57.41542+00	2021-12-23 10:06:08.487477+00	f	\N	103.67.158.16	876b4dde-d1f6-4e79-a513-b7375b2b954c
0bbc75a3-ae5d-44e0-a1d5-9e0fdfbc68e7	2021-12-23 10:06:37.739214+00	2021-12-23 10:13:02.80674+00	f	\N	103.67.158.16	2a2c60f1-e068-47d2-be66-88bd52116d20
b8f973d6-8b06-479d-9d33-7048f77d48a3	2021-12-23 10:20:07.398041+00	2021-12-23 14:03:20.228109+00	f	\N	102.89.0.142	8bf64794-80d0-4d64-bfc3-8a167f4f8960
68cd7746-aa47-49c4-9f09-646ca3f57318	2021-12-23 10:30:35.87877+00	2021-12-23 14:35:04.771738+00	f	\N	102.89.1.105	8bf64794-80d0-4d64-bfc3-8a167f4f8960
2321ff82-4f9b-41e1-8ac4-6f5cc56be5cd	2021-12-23 10:37:59.671201+00	2021-12-23 13:10:25.5148+00	f	\N	103.120.38.200	70b8af3e-d59d-48e7-90e6-ded64489cf7f
57ab66dd-8d7b-4b0a-bce0-d4ef57606959	2021-12-23 11:42:22.975854+00	2021-12-23 11:49:21.816431+00	f	\N	103.125.29.41	2a2c60f1-e068-47d2-be66-88bd52116d20
2150d954-a77d-4121-ac6c-4ffd05ec2c6d	2021-12-23 12:25:36.757848+00	2021-12-24 10:20:28.351404+00	f	\N	102.89.1.237	8bf64794-80d0-4d64-bfc3-8a167f4f8960
739ddeb1-0b88-4da3-8075-1d6720f9f502	2021-12-23 12:27:52.174803+00	2021-12-24 16:11:45.746216+00	f	\N	102.89.1.197	8bf64794-80d0-4d64-bfc3-8a167f4f8960
09b74da7-4c54-4690-a9af-4cdc3b930101	2021-12-23 12:29:19.308592+00	2021-12-23 13:17:16.119011+00	f	\N	103.125.29.41	70b8af3e-d59d-48e7-90e6-ded64489cf7f
0b26dc04-97c4-4ea1-bcec-e41d504216f1	2021-12-23 14:50:02.141343+00	2021-12-24 05:42:00.033276+00	f	\N	197.210.64.162	8bf64794-80d0-4d64-bfc3-8a167f4f8960
cd976f79-d806-4c67-855d-79b9afa5cd62	2021-12-24 01:45:11.200287+00	2021-12-24 12:19:23.999572+00	f	\N	102.89.0.112	8bf64794-80d0-4d64-bfc3-8a167f4f8960
09a865eb-4509-4c78-af65-f7092f636e77	2021-12-24 03:33:36.187353+00	2021-12-24 10:21:59.598533+00	f	\N	102.89.0.110	8bf64794-80d0-4d64-bfc3-8a167f4f8960
3b2e10f1-131e-4b58-ab24-e1aa927585b8	2021-12-24 11:03:49.012184+00	2021-12-24 11:03:49.599647+00	f	\N	102.89.0.191	8bf64794-80d0-4d64-bfc3-8a167f4f8960
1b528890-9940-4069-88a8-5ac743337032	2021-12-24 11:04:37.400112+00	2021-12-24 11:05:23.627769+00	f	\N	102.89.1.20	8bf64794-80d0-4d64-bfc3-8a167f4f8960
170e814d-7ca7-484d-b5f1-8602057109fc	2021-12-24 12:08:24.834236+00	2021-12-24 12:08:24.834269+00	f	\N	102.89.0.106	8bf64794-80d0-4d64-bfc3-8a167f4f8960
69e338c3-fa98-4db3-bccd-133e440e5296	2021-12-24 15:50:01.418659+00	2021-12-24 16:12:03.630789+00	f	\N	102.89.1.21	8bf64794-80d0-4d64-bfc3-8a167f4f8960
37c863de-28d3-436a-8839-e5623c64a228	2021-12-24 15:50:02.196705+00	2021-12-24 16:14:29.704928+00	f	\N	102.89.0.28	8bf64794-80d0-4d64-bfc3-8a167f4f8960
8680be8c-64b2-4219-ace5-62542d89839d	2021-12-25 10:20:16.366297+00	2021-12-25 10:20:16.366331+00	f	\N	197.210.65.233	6c0e20bd-57f4-48e6-a2bf-75319fef2cf3
6ec1316d-57a2-472e-88d6-21bb5c6047c9	2021-12-25 10:22:44.976427+00	2021-12-25 10:23:14.083933+00	f	\N	197.210.65.233	8bf64794-80d0-4d64-bfc3-8a167f4f8960
2ec95289-d4a8-40d5-9e2b-a5308f93bafc	2021-12-25 11:04:42.658647+00	2021-12-25 11:04:42.658683+00	f	\N	197.210.45.161	6c0e20bd-57f4-48e6-a2bf-75319fef2cf3
382a13fe-8a65-47f9-99b6-85f59eae2da2	2021-12-27 03:21:43.306094+00	2021-12-27 03:34:36.719286+00	f	\N	197.210.8.95	8bf64794-80d0-4d64-bfc3-8a167f4f8960
323f28cc-4c54-4475-acb1-8703a059bc8e	2021-12-27 06:54:02.240408+00	2021-12-27 06:55:20.145092+00	f	\N	103.125.29.41	db3fc55b-bd76-4ce6-9874-170ab76870ca
987bc4c9-2421-472e-abb6-d13114176e7c	2021-12-27 06:54:04.431037+00	2021-12-27 06:54:04.43108+00	f	\N	103.221.55.51	db3fc55b-bd76-4ce6-9874-170ab76870ca
2e7e4b28-3e3a-4a39-adce-f30aac80dc16	2021-12-27 07:11:19.717375+00	2021-12-27 07:47:23.397172+00	f	\N	103.112.236.77	235a9a51-9ceb-4b55-a687-46bc634eb0fa
0d706d7c-93f6-4e26-aab9-edbea50a86de	2021-12-27 07:13:53.157632+00	2021-12-27 07:48:13.693611+00	f	\N	103.112.236.77	e7556c15-90eb-42ab-b45c-0ab6cf333068
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sihan
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sihan
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sihan
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 152, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sihan
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sihan
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 38, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sihan
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 48, true);


--
-- Name: django_site_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sihan
--

SELECT pg_catalog.setval('public.django_site_id_seq', 1, true);


--
-- Name: ehr_icds_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sihan
--

SELECT pg_catalog.setval('public.ehr_icds_id_seq', 1, false);


--
-- Name: user_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sihan
--

SELECT pg_catalog.setval('public.user_user_groups_id_seq', 1, false);


--
-- Name: user_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sihan
--

SELECT pg_catalog.setval('public.user_user_user_permissions_id_seq', 1, false);


--
-- Name: appointment_appointment appointment_appointment_pkey; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.appointment_appointment
    ADD CONSTRAINT appointment_appointment_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: authtoken_token authtoken_token_pkey; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_pkey PRIMARY KEY (key);


--
-- Name: authtoken_token authtoken_token_user_id_key; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_key UNIQUE (user_id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: django_site django_site_domain_a2e37b91_uniq; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.django_site
    ADD CONSTRAINT django_site_domain_a2e37b91_uniq UNIQUE (domain);


--
-- Name: django_site django_site_pkey; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.django_site
    ADD CONSTRAINT django_site_pkey PRIMARY KEY (id);


--
-- Name: ehr_assessmentdiagnosis ehr_assessmentdiagnosis_pkey; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.ehr_assessmentdiagnosis
    ADD CONSTRAINT ehr_assessmentdiagnosis_pkey PRIMARY KEY (id);


--
-- Name: ehr_chiefcomplaintsandhpi ehr_chiefcomplaintsandhpi_pkey; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.ehr_chiefcomplaintsandhpi
    ADD CONSTRAINT ehr_chiefcomplaintsandhpi_pkey PRIMARY KEY (id);


--
-- Name: ehr_functionalandcognitivestatus ehr_functionalandcognitivestatus_pkey; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.ehr_functionalandcognitivestatus
    ADD CONSTRAINT ehr_functionalandcognitivestatus_pkey PRIMARY KEY (id);


--
-- Name: ehr_icds ehr_icds_pkey; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.ehr_icds
    ADD CONSTRAINT ehr_icds_pkey PRIMARY KEY (id);


--
-- Name: ehr_planofcare ehr_medicalnotes_pkey; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.ehr_planofcare
    ADD CONSTRAINT ehr_medicalnotes_pkey PRIMARY KEY (id);


--
-- Name: ehr_orders ehr_orders_pkey; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.ehr_orders
    ADD CONSTRAINT ehr_orders_pkey PRIMARY KEY (id);


--
-- Name: ehr_patientencounters ehr_patientencounters_pkey; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.ehr_patientencounters
    ADD CONSTRAINT ehr_patientencounters_pkey PRIMARY KEY (id);


--
-- Name: ehr_patientprocedure ehr_patientprocedure_pkey; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.ehr_patientprocedure
    ADD CONSTRAINT ehr_patientprocedure_pkey PRIMARY KEY (id);


--
-- Name: ehr_patientsocialhistory ehr_patientsocialhistory_pkey; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.ehr_patientsocialhistory
    ADD CONSTRAINT ehr_patientsocialhistory_pkey PRIMARY KEY (id);


--
-- Name: ehr_physicalexam ehr_physicalexam_pkey; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.ehr_physicalexam
    ADD CONSTRAINT ehr_physicalexam_pkey PRIMARY KEY (id);


--
-- Name: ehr_reviewofsystem ehr_reviewofsystem_pkey; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.ehr_reviewofsystem
    ADD CONSTRAINT ehr_reviewofsystem_pkey PRIMARY KEY (id);


--
-- Name: ehr_vitals ehr_vitals_pkey; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.ehr_vitals
    ADD CONSTRAINT ehr_vitals_pkey PRIMARY KEY (id);


--
-- Name: inbox_inboxchannel inbox_inboxchannel_pkey; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.inbox_inboxchannel
    ADD CONSTRAINT inbox_inboxchannel_pkey PRIMARY KEY (id);


--
-- Name: inbox_inboxmessage inbox_inboxmessage_pkey; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.inbox_inboxmessage
    ADD CONSTRAINT inbox_inboxmessage_pkey PRIMARY KEY (id);


--
-- Name: twilio_chat_waitingroom twilio_chat_waitingroom_doctor_id_key; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.twilio_chat_waitingroom
    ADD CONSTRAINT twilio_chat_waitingroom_doctor_id_key UNIQUE (doctor_id);


--
-- Name: twilio_chat_waitingroom twilio_chat_waitingroom_pkey; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.twilio_chat_waitingroom
    ADD CONSTRAINT twilio_chat_waitingroom_pkey PRIMARY KEY (id);


--
-- Name: user_clinicinfo user_clinicinfo_pkey; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_clinicinfo
    ADD CONSTRAINT user_clinicinfo_pkey PRIMARY KEY (id);


--
-- Name: user_clinicinfo user_clinicinfo_user_id_key; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_clinicinfo
    ADD CONSTRAINT user_clinicinfo_user_id_key UNIQUE (user_id);


--
-- Name: user_clinicinfo user_clinicinfo_username_key; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_clinicinfo
    ADD CONSTRAINT user_clinicinfo_username_key UNIQUE (username);


--
-- Name: user_doctoracceptedinsurance user_doctoracceptedinsurance_pkey; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_doctoracceptedinsurance
    ADD CONSTRAINT user_doctoracceptedinsurance_pkey PRIMARY KEY (id);


--
-- Name: user_doctoravailablehours user_doctoravailablehours_pkey; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_doctoravailablehours
    ADD CONSTRAINT user_doctoravailablehours_pkey PRIMARY KEY (id);


--
-- Name: user_doctoreducation user_doctoreducation_pkey; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_doctoreducation
    ADD CONSTRAINT user_doctoreducation_pkey PRIMARY KEY (id);


--
-- Name: user_doctorexperience user_doctorexperience_pkey; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_doctorexperience
    ADD CONSTRAINT user_doctorexperience_pkey PRIMARY KEY (id);


--
-- Name: user_doctorinfo user_doctorinfo_pkey; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_doctorinfo
    ADD CONSTRAINT user_doctorinfo_pkey PRIMARY KEY (id);


--
-- Name: user_doctorinfo user_doctorinfo_user_id_key; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_doctorinfo
    ADD CONSTRAINT user_doctorinfo_user_id_key UNIQUE (user_id);


--
-- Name: user_doctorinfo user_doctorinfo_username_key; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_doctorinfo
    ADD CONSTRAINT user_doctorinfo_username_key UNIQUE (username);


--
-- Name: user_doctorlanguage user_doctorlanguage_pkey; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_doctorlanguage
    ADD CONSTRAINT user_doctorlanguage_pkey PRIMARY KEY (id);


--
-- Name: user_doctorreview user_doctorreview_pkey; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_doctorreview
    ADD CONSTRAINT user_doctorreview_pkey PRIMARY KEY (id);


--
-- Name: user_doctorspecialty user_doctorspecialty_pkey; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_doctorspecialty
    ADD CONSTRAINT user_doctorspecialty_pkey PRIMARY KEY (id);


--
-- Name: user_passwordresetwhitelist user_passwordresetwhitelist_email_key; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_passwordresetwhitelist
    ADD CONSTRAINT user_passwordresetwhitelist_email_key UNIQUE (email);


--
-- Name: user_passwordresetwhitelist user_passwordresetwhitelist_pkey; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_passwordresetwhitelist
    ADD CONSTRAINT user_passwordresetwhitelist_pkey PRIMARY KEY (id);


--
-- Name: user_passwordresetwhitelist user_passwordresetwhitelist_token_key; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_passwordresetwhitelist
    ADD CONSTRAINT user_passwordresetwhitelist_token_key UNIQUE (token);


--
-- Name: user_patientinfo user_patientinfo_pkey; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_patientinfo
    ADD CONSTRAINT user_patientinfo_pkey PRIMARY KEY (id);


--
-- Name: user_patientinfo user_patientinfo_user_id_key; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_patientinfo
    ADD CONSTRAINT user_patientinfo_user_id_key UNIQUE (user_id);


--
-- Name: user_pharmacyinfo user_pharmacyinfo_pkey; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_pharmacyinfo
    ADD CONSTRAINT user_pharmacyinfo_pkey PRIMARY KEY (id);


--
-- Name: user_pharmacyinfo user_pharmacyinfo_user_id_key; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_pharmacyinfo
    ADD CONSTRAINT user_pharmacyinfo_user_id_key UNIQUE (user_id);


--
-- Name: user_pharmacyinfo user_pharmacyinfo_username_key; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_pharmacyinfo
    ADD CONSTRAINT user_pharmacyinfo_username_key UNIQUE (username);


--
-- Name: user_user user_user_email_key; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_user
    ADD CONSTRAINT user_user_email_key UNIQUE (email);


--
-- Name: user_user_groups user_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_user_groups
    ADD CONSTRAINT user_user_groups_pkey PRIMARY KEY (id);


--
-- Name: user_user_groups user_user_groups_user_id_group_id_bb60391f_uniq; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_user_groups
    ADD CONSTRAINT user_user_groups_user_id_group_id_bb60391f_uniq UNIQUE (user_id, group_id);


--
-- Name: user_user user_user_pkey; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_user
    ADD CONSTRAINT user_user_pkey PRIMARY KEY (id);


--
-- Name: user_user_user_permissions user_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_user_user_permissions
    ADD CONSTRAINT user_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: user_user_user_permissions user_user_user_permissions_user_id_permission_id_64f4d5b8_uniq; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_user_user_permissions
    ADD CONSTRAINT user_user_user_permissions_user_id_permission_id_64f4d5b8_uniq UNIQUE (user_id, permission_id);


--
-- Name: user_userip user_userip_pkey; Type: CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_userip
    ADD CONSTRAINT user_userip_pkey PRIMARY KEY (id);


--
-- Name: appointment_appointment_doctor_id_5325109f; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX appointment_appointment_doctor_id_5325109f ON public.appointment_appointment USING btree (doctor_id);


--
-- Name: appointment_appointment_patient_id_893eaa7b; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX appointment_appointment_patient_id_893eaa7b ON public.appointment_appointment USING btree (patient_id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: authtoken_token_key_10f0b77e_like; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX authtoken_token_key_10f0b77e_like ON public.authtoken_token USING btree (key varchar_pattern_ops);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: django_site_domain_a2e37b91_like; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX django_site_domain_a2e37b91_like ON public.django_site USING btree (domain varchar_pattern_ops);


--
-- Name: ehr_assessmentdiagnosis_patient_encounter_id_32301d56; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX ehr_assessmentdiagnosis_patient_encounter_id_32301d56 ON public.ehr_assessmentdiagnosis USING btree (patient_encounter_id);


--
-- Name: ehr_chiefcomplaintsandhpi_patient_encounter_id_78d364c0; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX ehr_chiefcomplaintsandhpi_patient_encounter_id_78d364c0 ON public.ehr_chiefcomplaintsandhpi USING btree (patient_encounter_id);


--
-- Name: ehr_functionalandcognitivestatus_patient_encounter_id_a315ecd0; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX ehr_functionalandcognitivestatus_patient_encounter_id_a315ecd0 ON public.ehr_functionalandcognitivestatus USING btree (patient_encounter_id);


--
-- Name: ehr_medicalnotes_patient_encounter_id_f809f9b2; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX ehr_medicalnotes_patient_encounter_id_f809f9b2 ON public.ehr_planofcare USING btree (patient_encounter_id);


--
-- Name: ehr_orders_patient_encounter_id_fa0c3e2a; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX ehr_orders_patient_encounter_id_fa0c3e2a ON public.ehr_orders USING btree (patient_encounter_id);


--
-- Name: ehr_patientencounters_patient_id_62a228c5; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX ehr_patientencounters_patient_id_62a228c5 ON public.ehr_patientencounters USING btree (patient_id);


--
-- Name: ehr_patientencounters_provider_id_3ddc30c6; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX ehr_patientencounters_provider_id_3ddc30c6 ON public.ehr_patientencounters USING btree (provider_id);


--
-- Name: ehr_patientprocedure_patient_encounter_id_498fbadc; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX ehr_patientprocedure_patient_encounter_id_498fbadc ON public.ehr_patientprocedure USING btree (patient_encounter_id);


--
-- Name: ehr_patientsocialhistory_patient_encounter_id_c864dfb0; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX ehr_patientsocialhistory_patient_encounter_id_c864dfb0 ON public.ehr_patientsocialhistory USING btree (patient_encounter_id);


--
-- Name: ehr_physicalexam_patient_encounter_id_931ea8af; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX ehr_physicalexam_patient_encounter_id_931ea8af ON public.ehr_physicalexam USING btree (patient_encounter_id);


--
-- Name: ehr_reviewofsystem_patient_encounter_id_e516f3f2; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX ehr_reviewofsystem_patient_encounter_id_e516f3f2 ON public.ehr_reviewofsystem USING btree (patient_encounter_id);


--
-- Name: ehr_vitals_patient_encounter_id_b5413116; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX ehr_vitals_patient_encounter_id_b5413116 ON public.ehr_vitals USING btree (patient_encounter_id);


--
-- Name: inbox_inboxchannel_first_user_id_6f3d850b; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX inbox_inboxchannel_first_user_id_6f3d850b ON public.inbox_inboxchannel USING btree (first_user_id);


--
-- Name: inbox_inboxchannel_second_user_id_edc68720; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX inbox_inboxchannel_second_user_id_edc68720 ON public.inbox_inboxchannel USING btree (second_user_id);


--
-- Name: inbox_inboxmessage_channel_id_1074b32b; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX inbox_inboxmessage_channel_id_1074b32b ON public.inbox_inboxmessage USING btree (channel_id);


--
-- Name: inbox_inboxmessage_sender_id_08545433; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX inbox_inboxmessage_sender_id_08545433 ON public.inbox_inboxmessage USING btree (sender_id);


--
-- Name: user_clinicinfo_username_3ac93cc1_like; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX user_clinicinfo_username_3ac93cc1_like ON public.user_clinicinfo USING btree (username varchar_pattern_ops);


--
-- Name: user_doctoracceptedinsurance_doctor_info_id_51ec976c; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX user_doctoracceptedinsurance_doctor_info_id_51ec976c ON public.user_doctoracceptedinsurance USING btree (doctor_info_id);


--
-- Name: user_doctoravailablehours_doctor_info_id_30b21f62; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX user_doctoravailablehours_doctor_info_id_30b21f62 ON public.user_doctoravailablehours USING btree (doctor_info_id);


--
-- Name: user_doctoreducation_doctor_info_id_cda3bc40; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX user_doctoreducation_doctor_info_id_cda3bc40 ON public.user_doctoreducation USING btree (doctor_info_id);


--
-- Name: user_doctorexperience_doctor_info_id_3ce2bdb8; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX user_doctorexperience_doctor_info_id_3ce2bdb8 ON public.user_doctorexperience USING btree (doctor_info_id);


--
-- Name: user_doctorinfo_username_5e9bbea7_like; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX user_doctorinfo_username_5e9bbea7_like ON public.user_doctorinfo USING btree (username varchar_pattern_ops);


--
-- Name: user_doctorlanguage_doctor_info_id_231d88ed; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX user_doctorlanguage_doctor_info_id_231d88ed ON public.user_doctorlanguage USING btree (doctor_info_id);


--
-- Name: user_doctorreview_doctor_info_id_cd9cf353; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX user_doctorreview_doctor_info_id_cd9cf353 ON public.user_doctorreview USING btree (doctor_info_id);


--
-- Name: user_doctorspecialty_doctor_info_id_e499cda2; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX user_doctorspecialty_doctor_info_id_e499cda2 ON public.user_doctorspecialty USING btree (doctor_info_id);


--
-- Name: user_passwordresetwhitelist_email_863d34ad_like; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX user_passwordresetwhitelist_email_863d34ad_like ON public.user_passwordresetwhitelist USING btree (email varchar_pattern_ops);


--
-- Name: user_passwordresetwhitelist_token_8fb90b0a_like; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX user_passwordresetwhitelist_token_8fb90b0a_like ON public.user_passwordresetwhitelist USING btree (token varchar_pattern_ops);


--
-- Name: user_pharmacyinfo_username_b52fe15a_like; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX user_pharmacyinfo_username_b52fe15a_like ON public.user_pharmacyinfo USING btree (username varchar_pattern_ops);


--
-- Name: user_user_email_1c6f3d1a_like; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX user_user_email_1c6f3d1a_like ON public.user_user USING btree (email varchar_pattern_ops);


--
-- Name: user_user_groups_group_id_c57f13c0; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX user_user_groups_group_id_c57f13c0 ON public.user_user_groups USING btree (group_id);


--
-- Name: user_user_groups_user_id_13f9a20d; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX user_user_groups_user_id_13f9a20d ON public.user_user_groups USING btree (user_id);


--
-- Name: user_user_user_permissions_permission_id_ce49d4de; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX user_user_user_permissions_permission_id_ce49d4de ON public.user_user_user_permissions USING btree (permission_id);


--
-- Name: user_user_user_permissions_user_id_31782f58; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX user_user_user_permissions_user_id_31782f58 ON public.user_user_user_permissions USING btree (user_id);


--
-- Name: user_userip_user_id_379a2318; Type: INDEX; Schema: public; Owner: sihan
--

CREATE INDEX user_userip_user_id_379a2318 ON public.user_userip USING btree (user_id);


--
-- Name: appointment_appointment appointment_appointm_doctor_id_5325109f_fk_user_doct; Type: FK CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.appointment_appointment
    ADD CONSTRAINT appointment_appointm_doctor_id_5325109f_fk_user_doct FOREIGN KEY (doctor_id) REFERENCES public.user_doctorinfo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: appointment_appointment appointment_appointm_patient_id_893eaa7b_fk_user_pati; Type: FK CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.appointment_appointment
    ADD CONSTRAINT appointment_appointm_patient_id_893eaa7b_fk_user_pati FOREIGN KEY (patient_id) REFERENCES public.user_patientinfo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: authtoken_token authtoken_token_user_id_35299eff_fk_user_user_id; Type: FK CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_35299eff_fk_user_user_id FOREIGN KEY (user_id) REFERENCES public.user_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_user_user_id; Type: FK CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_user_user_id FOREIGN KEY (user_id) REFERENCES public.user_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ehr_assessmentdiagnosis ehr_assessmentdiagno_patient_encounter_id_32301d56_fk_ehr_patie; Type: FK CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.ehr_assessmentdiagnosis
    ADD CONSTRAINT ehr_assessmentdiagno_patient_encounter_id_32301d56_fk_ehr_patie FOREIGN KEY (patient_encounter_id) REFERENCES public.ehr_patientencounters(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ehr_chiefcomplaintsandhpi ehr_chiefcomplaintsa_patient_encounter_id_78d364c0_fk_ehr_patie; Type: FK CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.ehr_chiefcomplaintsandhpi
    ADD CONSTRAINT ehr_chiefcomplaintsa_patient_encounter_id_78d364c0_fk_ehr_patie FOREIGN KEY (patient_encounter_id) REFERENCES public.ehr_patientencounters(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ehr_functionalandcognitivestatus ehr_functionalandcog_patient_encounter_id_a315ecd0_fk_ehr_patie; Type: FK CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.ehr_functionalandcognitivestatus
    ADD CONSTRAINT ehr_functionalandcog_patient_encounter_id_a315ecd0_fk_ehr_patie FOREIGN KEY (patient_encounter_id) REFERENCES public.ehr_patientencounters(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ehr_planofcare ehr_medicalnotes_patient_encounter_id_f809f9b2_fk_ehr_patie; Type: FK CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.ehr_planofcare
    ADD CONSTRAINT ehr_medicalnotes_patient_encounter_id_f809f9b2_fk_ehr_patie FOREIGN KEY (patient_encounter_id) REFERENCES public.ehr_patientencounters(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ehr_orders ehr_orders_patient_encounter_id_fa0c3e2a_fk_ehr_patie; Type: FK CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.ehr_orders
    ADD CONSTRAINT ehr_orders_patient_encounter_id_fa0c3e2a_fk_ehr_patie FOREIGN KEY (patient_encounter_id) REFERENCES public.ehr_patientencounters(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ehr_patientencounters ehr_patientencounter_patient_id_62a228c5_fk_user_pati; Type: FK CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.ehr_patientencounters
    ADD CONSTRAINT ehr_patientencounter_patient_id_62a228c5_fk_user_pati FOREIGN KEY (patient_id) REFERENCES public.user_patientinfo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ehr_patientencounters ehr_patientencounter_provider_id_3ddc30c6_fk_user_doct; Type: FK CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.ehr_patientencounters
    ADD CONSTRAINT ehr_patientencounter_provider_id_3ddc30c6_fk_user_doct FOREIGN KEY (provider_id) REFERENCES public.user_doctorinfo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ehr_patientprocedure ehr_patientprocedure_patient_encounter_id_498fbadc_fk_ehr_patie; Type: FK CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.ehr_patientprocedure
    ADD CONSTRAINT ehr_patientprocedure_patient_encounter_id_498fbadc_fk_ehr_patie FOREIGN KEY (patient_encounter_id) REFERENCES public.ehr_patientencounters(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ehr_patientsocialhistory ehr_patientsocialhis_patient_encounter_id_c864dfb0_fk_ehr_patie; Type: FK CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.ehr_patientsocialhistory
    ADD CONSTRAINT ehr_patientsocialhis_patient_encounter_id_c864dfb0_fk_ehr_patie FOREIGN KEY (patient_encounter_id) REFERENCES public.ehr_patientencounters(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ehr_physicalexam ehr_physicalexam_patient_encounter_id_931ea8af_fk_ehr_patie; Type: FK CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.ehr_physicalexam
    ADD CONSTRAINT ehr_physicalexam_patient_encounter_id_931ea8af_fk_ehr_patie FOREIGN KEY (patient_encounter_id) REFERENCES public.ehr_patientencounters(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ehr_reviewofsystem ehr_reviewofsystem_patient_encounter_id_e516f3f2_fk_ehr_patie; Type: FK CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.ehr_reviewofsystem
    ADD CONSTRAINT ehr_reviewofsystem_patient_encounter_id_e516f3f2_fk_ehr_patie FOREIGN KEY (patient_encounter_id) REFERENCES public.ehr_patientencounters(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ehr_vitals ehr_vitals_patient_encounter_id_b5413116_fk_ehr_patie; Type: FK CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.ehr_vitals
    ADD CONSTRAINT ehr_vitals_patient_encounter_id_b5413116_fk_ehr_patie FOREIGN KEY (patient_encounter_id) REFERENCES public.ehr_patientencounters(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: inbox_inboxchannel inbox_inboxchannel_first_user_id_6f3d850b_fk_user_user_id; Type: FK CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.inbox_inboxchannel
    ADD CONSTRAINT inbox_inboxchannel_first_user_id_6f3d850b_fk_user_user_id FOREIGN KEY (first_user_id) REFERENCES public.user_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: inbox_inboxchannel inbox_inboxchannel_second_user_id_edc68720_fk_user_user_id; Type: FK CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.inbox_inboxchannel
    ADD CONSTRAINT inbox_inboxchannel_second_user_id_edc68720_fk_user_user_id FOREIGN KEY (second_user_id) REFERENCES public.user_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: inbox_inboxmessage inbox_inboxmessage_channel_id_1074b32b_fk_inbox_inboxchannel_id; Type: FK CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.inbox_inboxmessage
    ADD CONSTRAINT inbox_inboxmessage_channel_id_1074b32b_fk_inbox_inboxchannel_id FOREIGN KEY (channel_id) REFERENCES public.inbox_inboxchannel(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: inbox_inboxmessage inbox_inboxmessage_sender_id_08545433_fk_user_user_id; Type: FK CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.inbox_inboxmessage
    ADD CONSTRAINT inbox_inboxmessage_sender_id_08545433_fk_user_user_id FOREIGN KEY (sender_id) REFERENCES public.user_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: twilio_chat_waitingroom twilio_chat_waitingr_doctor_id_84df698a_fk_user_doct; Type: FK CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.twilio_chat_waitingroom
    ADD CONSTRAINT twilio_chat_waitingr_doctor_id_84df698a_fk_user_doct FOREIGN KEY (doctor_id) REFERENCES public.user_doctorinfo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_clinicinfo user_clinicinfo_user_id_7a39e242_fk_user_user_id; Type: FK CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_clinicinfo
    ADD CONSTRAINT user_clinicinfo_user_id_7a39e242_fk_user_user_id FOREIGN KEY (user_id) REFERENCES public.user_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_doctoracceptedinsurance user_doctoracceptedi_doctor_info_id_51ec976c_fk_user_doct; Type: FK CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_doctoracceptedinsurance
    ADD CONSTRAINT user_doctoracceptedi_doctor_info_id_51ec976c_fk_user_doct FOREIGN KEY (doctor_info_id) REFERENCES public.user_doctorinfo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_doctoravailablehours user_doctoravailable_doctor_info_id_30b21f62_fk_user_doct; Type: FK CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_doctoravailablehours
    ADD CONSTRAINT user_doctoravailable_doctor_info_id_30b21f62_fk_user_doct FOREIGN KEY (doctor_info_id) REFERENCES public.user_doctorinfo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_doctoreducation user_doctoreducation_doctor_info_id_cda3bc40_fk_user_doct; Type: FK CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_doctoreducation
    ADD CONSTRAINT user_doctoreducation_doctor_info_id_cda3bc40_fk_user_doct FOREIGN KEY (doctor_info_id) REFERENCES public.user_doctorinfo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_doctorexperience user_doctorexperienc_doctor_info_id_3ce2bdb8_fk_user_doct; Type: FK CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_doctorexperience
    ADD CONSTRAINT user_doctorexperienc_doctor_info_id_3ce2bdb8_fk_user_doct FOREIGN KEY (doctor_info_id) REFERENCES public.user_doctorinfo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_doctorinfo user_doctorinfo_user_id_64faf23e_fk_user_user_id; Type: FK CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_doctorinfo
    ADD CONSTRAINT user_doctorinfo_user_id_64faf23e_fk_user_user_id FOREIGN KEY (user_id) REFERENCES public.user_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_doctorlanguage user_doctorlanguage_doctor_info_id_231d88ed_fk_user_doct; Type: FK CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_doctorlanguage
    ADD CONSTRAINT user_doctorlanguage_doctor_info_id_231d88ed_fk_user_doct FOREIGN KEY (doctor_info_id) REFERENCES public.user_doctorinfo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_doctorreview user_doctorreview_doctor_info_id_cd9cf353_fk_user_doctorinfo_id; Type: FK CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_doctorreview
    ADD CONSTRAINT user_doctorreview_doctor_info_id_cd9cf353_fk_user_doctorinfo_id FOREIGN KEY (doctor_info_id) REFERENCES public.user_doctorinfo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_doctorspecialty user_doctorspecialty_doctor_info_id_e499cda2_fk_user_doct; Type: FK CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_doctorspecialty
    ADD CONSTRAINT user_doctorspecialty_doctor_info_id_e499cda2_fk_user_doct FOREIGN KEY (doctor_info_id) REFERENCES public.user_doctorinfo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_patientinfo user_patientinfo_user_id_59fbb495_fk_user_user_id; Type: FK CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_patientinfo
    ADD CONSTRAINT user_patientinfo_user_id_59fbb495_fk_user_user_id FOREIGN KEY (user_id) REFERENCES public.user_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_pharmacyinfo user_pharmacyinfo_user_id_669cf350_fk_user_user_id; Type: FK CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_pharmacyinfo
    ADD CONSTRAINT user_pharmacyinfo_user_id_669cf350_fk_user_user_id FOREIGN KEY (user_id) REFERENCES public.user_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_user_groups user_user_groups_group_id_c57f13c0_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_user_groups
    ADD CONSTRAINT user_user_groups_group_id_c57f13c0_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_user_groups user_user_groups_user_id_13f9a20d_fk_user_user_id; Type: FK CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_user_groups
    ADD CONSTRAINT user_user_groups_user_id_13f9a20d_fk_user_user_id FOREIGN KEY (user_id) REFERENCES public.user_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_user_user_permissions user_user_user_permi_permission_id_ce49d4de_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_user_user_permissions
    ADD CONSTRAINT user_user_user_permi_permission_id_ce49d4de_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_user_user_permissions user_user_user_permissions_user_id_31782f58_fk_user_user_id; Type: FK CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_user_user_permissions
    ADD CONSTRAINT user_user_user_permissions_user_id_31782f58_fk_user_user_id FOREIGN KEY (user_id) REFERENCES public.user_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_userip user_userip_user_id_379a2318_fk_user_user_id; Type: FK CONSTRAINT; Schema: public; Owner: sihan
--

ALTER TABLE ONLY public.user_userip
    ADD CONSTRAINT user_userip_user_id_379a2318_fk_user_user_id FOREIGN KEY (user_id) REFERENCES public.user_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

