CREATE SCHEMA dimension;


CREATE TABLE dimension.stay_type(
    stay_type_id INT PRIMARY KEY,
    stay_type_name VARCHAR(255)
);


INSERT INTO dimension.stay_type (stay_type_id, stay_type_name)
VALUES
(1, '모텔'),
(2, '호텔'),
(3, '펜션'),
(4, '게스트하우스');

drop table dimension.room_type;
CREATE TABLE dimension.room_type (
    stay_type_id INT,
    room_type_id INT,
    room_type_name VARCHAR(255),
    PRIMARY KEY (stay_type_id, room_type_id),
    FOREIGN KEY (stay_type_id) REFERENCES dimension.stay_type(stay_type_id)
);

INSERT INTO dimension.room_type (stay_type_id, room_type_id, room_type_name)
VALUES
(1, 1, '일반실'),
(1, 2, '준특실'),
(1, 3, '특실'),
(1, 4, 'VIP실'),
(1, 5, 'VVIP실'),
(2, 1, '스탠다드'),
(2, 2, '트윈'),
(2, 3, '스위트'),
(2, 4, '디럭스'),
(2, 5, '프리미엄'),
(3, 1, '일반실'),
(3, 2, '가족실'),
(4, 1, '도미토리 남성'),
(4, 2, '도미토리 여성'),
(4, 3, '단체룸');

create table stay_info
(
    stay_seq                  serial
        primary key,
    stay_name                 varchar(255),
    manager                   varchar(255),
    contact_number            varchar(50),
    address                   text,
    check_in_time             time,
    check_in_additional_info  text,
    check_out_time            time,
    check_out_additional_info text,
    description               text,
    stay_scale                text,
    capacity                  integer,
    room_count                integer,
    room_type                 varchar(255),
    refund_policy             text,
    homepage_url              varchar(255),
    reservation_info          varchar(255),
    pickup_available          boolean,
    pickup_additional_info    varchar(255),
    parking_available         boolean,
    parking_count             integer,
    cook_available            boolean,
    korea_tourism_certified   boolean,
    seminar_facilities        boolean,
    sports_facilities         boolean,
    sauna_facilities          boolean,
    beauty_facilities         boolean,
    karaoke_facilities        boolean,
    barbecue_facilities       boolean,
    campfire_facilities       boolean,
    fitness_center_facilities boolean,
    internet_cafe_facilities  boolean,
    public_shower_facilities  boolean,
    bike_rental               boolean,
    latitude                  numeric(10, 7),
    longitude                 numeric(10, 7),
    postal_code               varchar(20),
    stay_detail               text,
    facilities_detail         text,
    food_beverage_area        text,
    created_at                timestamp default now() not null,
    modified_at               timestamp default now() not null
);

create table room_info
(
    room_seq            serial
        primary key,
    stay_seq            integer,
    stay_name           text,
    stay_type           integer,
    room_name           text,
    room_type           integer,
    room_price          integer,
    room_available_count integer,
    room_image_url_list text,
    ott_service         text,
    toilet_option       text,
    room_option         text,
    special_room_option text
);

create table public.wish
(
    wish_seq serial
        primary key,
    user_seq bigint,
    stay_seq bigint,
    state character(1),
    wished_at timestamp default now(),
    modified_at timestamp
);

ALTER TABLE public.wish
ADD CONSTRAINT user_seq_stay_seq_constraint UNIQUE (user_seq, stay_seq);

create table public.review
(
    review_seq serial
        primary key,
    user_seq bigint,
    stay_seq bigint,
    room_seq bigint,
    review_title text,
    review_content text,
    review_score integer,
    review_image_url_list text,
    created_at timestamp default now(),
    modified_at timestamp default now()
);
create index user_seq_index
    on public.review (user_seq);
create index stay_seq_index
    on public.review (stay_seq);
create index room_seq_index
    on public.review (room_seq);

ALTER TABLE public.review ADD column exposed boolean default true;

create table public.reservation
(
    reservation_seq serial
        primary key,
    user_seq bigint,
    stay_seq bigint,
    room_seq bigint,
    check_in_date date,
    check_out_date date,
    reservation_price integer,
    reservation_status character(1),
    reservation_date timestamp default now(),
    modified_at timestamp default now()
);



CREATE TABLE IF NOT EXISTS "users"
(
    "user_seq"        SERIAL PRIMARY KEY         NOT NULL,
    "user_name"       VARCHAR(255) UNIQUE        NOT NULL,
    "user_email"      VARCHAR(255) UNIQUE        NOT NULL,
    "gender"          CHAR(1)                    NOT NULL,
    "birth_at"        TIMESTAMP(0)               NULL,
    "created_at"      TIMESTAMP(0) DEFAULT NOW() NOT NULL,
    "updated_at"      TIMESTAMP(0)               NULL,
    "deleted_at"      TIMESTAMP(0)               NULL,
    "image"           TEXT                       NULL,
    "service_agree"   BOOLEAN                    NOT NULL,
    "location_agree"  BOOLEAN                    NULL,
    "marketing_agree" BOOLEAN                    NULL
);


CREATE TABLE IF NOT EXISTS "accounts"
(
    "account_seq"   SERIAL PRIMARY KEY         NOT NULL,
    "provider_type" VARCHAR(255)               NOT NULL,
    "created_at"    TIMESTAMP(0) DEFAULT NOW() NOT NULL,
    "updated_at"    TIMESTAMP(0)               NULL,
    "deleted_at"    TIMESTAMP(0)               NULL,
    "email"         VARCHAR(255)               NOT NULL,
    "user_seq"      SERIAL                     NOT NULL
);
ALTER TABLE
    "accounts"
    ADD CONSTRAINT "accounts_user_seq_foreign" FOREIGN KEY ("user_seq") REFERENCES "users" ("user_seq");



select * from users;
select * from accounts;

DROP TABLE "accounts";
DROP TABLE "users";






