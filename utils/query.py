GET_USERS = (
    "select "
    "u.id as id, "
    "u.username as username, "
    "u.email as email, "
    "u.password as password, "
    "u.status as status, "
    "r.sender as sender, "
    "r.message_type as message_type "
    "from users u left outer join relation r on u.email = r.receiver order by u.id;"
)
