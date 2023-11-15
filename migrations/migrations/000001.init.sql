create table users (
    id bigserial primary key,
    name text not null
);
create table books (
    id bigserial primary key,
    user_id bigint not null references users(id) on delete cascade,
    title text not null
);
