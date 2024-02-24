create table users
(
    id         serial
        primary key,
    username   varchar(50) not null,
    email      varchar(50) not null
        unique,
    password   varchar(50) default NULL::character varying,
    status     boolean     default true,
    created_at timestamp   default CURRENT_TIMESTAMP
);
create table template
(
    id       serial
        primary key,
    type     varchar(20) not null
        unique,
    template varchar(1000),
    subject  varchar(100) default NULL::character varying
);
create table relation
(
    id           serial
        primary key,
    sender       varchar(50)
        references users (email),
    receiver     varchar(50)
        references users (email),
    message_type varchar(20) not null
        references template (type)
);