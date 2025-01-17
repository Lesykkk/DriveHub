#include "database.h"

Transport::Transport(const std::string& title, const std::string& image, double engine_volume, unsigned int mileage, unsigned int weight, unsigned int year)
    : title(title), image(image), engine_volume(engine_volume), mileage(mileage), weight(weight), year(year) { }

Transport::~Transport() { }

Car::Car(const std::string& title, const std::string& image, double engine_volume, unsigned int mileage, unsigned int weight, unsigned int year, unsigned int seat_number)
    : Transport(title, image, engine_volume, mileage, weight, year), seat_number(seat_number) { }

Truck::Truck(const std::string& title, const std::string& image, double engine_volume, unsigned int mileage, unsigned int weight, unsigned int year, unsigned int load_capacity)
    : Transport(title, image, engine_volume, mileage, weight, year), load_capacity(load_capacity) { }

Boat::Boat(const std::string& title, const std::string& image, double engine_volume, unsigned int mileage, unsigned int weight, unsigned int year, unsigned int propeller_number)
    : Transport(title, image, engine_volume, mileage, weight, year), propeller_number(propeller_number) { }

Account::Account(const std::string& username, const std::string& password, const std::string& first_name, const std::string& last_name, const std::string& email, const std::string& phone)
    : username(username), password(password), first_name(first_name), last_name(last_name), email(email), phone(phone) { }

Advert::Advert(Account* account, Transport* transport, const std::string& slug, unsigned int price, const std::string& city, const std::string& description, const std::string& created, const std::string& updated)
    : account(account), transport(transport), slug(slug), price(price), city(city), description(description), created(created), updated(updated) { }

std::string Advert::get_absolute_url() {
    return "/" + slug + "/";
}

Database::Database(const std::string& db_name) {
    if (sqlite3_open(db_name.c_str(), &db)) {
        std::cerr << "Can't open database: " << sqlite3_errmsg(db) << std::endl;
        db = nullptr;
    }
}

Database::~Database() {
    if (db) {
        sqlite3_close(db);
    }
}

std::list<Advert> Database::get_adverts(const std::string& _username, const std::string& _sort_by, const std::string& _transport_type,
        const std::string& _title, unsigned int _year, const std::string& _city,
        unsigned int _min_price, unsigned int _max_price) {
    std::list<Advert> adverts;
    
    std::string query =
        "SELECT a.slug, a.price, a.city, a.description, a.created, a.updated,"
        "ac.username, ac.password, ac.first_name, ac.last_name, ac.email, ac.phone, "
        "t.title, t.image, t.engine_volume, t.mileage, t.weight, t.year, "
        "CASE "
        "WHEN tc.transport_ptr_id IS NOT NULL THEN 'car' "
        "WHEN tt.transport_ptr_id IS NOT NULL THEN 'truck' "
        "WHEN tb.transport_ptr_id IS NOT NULL THEN 'boat' "
        "END AS transport_type, "
        "tc.seat_number, tt.load_capacity, tb.propeller_number "
        "FROM main_advert a "
        "JOIN account ac ON a.account_id = ac.id "
        "JOIN main_transport t ON a.transport_id = t.id "
        "LEFT JOIN main_car tc ON t.id = tc.transport_ptr_id "
        "LEFT JOIN main_truck tt ON t.id = tt.transport_ptr_id "
        "LEFT JOIN main_boat tb ON t.id = tb.transport_ptr_id "
        "WHERE 1=1";
    
    if (!_username.empty()) {
        query += " AND ac.username = '" + _username + "'";
    }
    if (!_title.empty()) {
        query += " AND t.title LIKE '%" + _title + "%'";
    }
    if (_transport_type != "all") {
        query += " AND CASE "
            "WHEN tc.transport_ptr_id IS NOT NULL THEN 'car' "
            "WHEN tt.transport_ptr_id IS NOT NULL THEN 'truck' "
            "WHEN tb.transport_ptr_id IS NOT NULL THEN 'boat' "
            "END = '" + _transport_type + "'";
    }
    if (_year > 0) {
        query += " AND t.year = " + std::to_string(_year);
    }
    if (!_city.empty()) {
        query += " AND a.city LIKE '%" + _city + "%'";
    }
    if (_min_price > 0) {
        query += " AND a.price >= " + std::to_string(_min_price);
    }
    if (_max_price > 0) {
        query += " AND a.price <= " + std::to_string(_max_price);
    }
    
    
    sqlite3_stmt* stmt;
    if (sqlite3_prepare_v2(db, query.c_str(), -1, &stmt, nullptr) != SQLITE_OK) {
        std::cerr << "Failed to fetch adverts: " << sqlite3_errmsg(db) << std::endl;
        return adverts;
    }
    
    while (sqlite3_step(stmt) == SQLITE_ROW) {
        std::string slug = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 0));
        unsigned int price = sqlite3_column_int(stmt, 1);
        std::string city = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 2));
        std::string description = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 3));
        std::string created = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 4));
        std::string updated = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 5));
    
        std::string username = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 6));
        std::string password = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 7));
        std::string first_name = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 8));
        std::string last_name = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 9));
        std::string email = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 10));
        std::string phone = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 11));
    
        std::string title = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 12));
        std::string image = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 13));
        double engine_volume = sqlite3_column_double(stmt, 14);
        unsigned int mileage = sqlite3_column_int(stmt, 15);
        unsigned int weight = sqlite3_column_int(stmt, 16);
        unsigned int year = sqlite3_column_int(stmt, 17);
    
        std::string transport_type = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 18));
    
        Account* account = new Account(username, password, first_name, last_name, email, phone);
        Transport* transport = nullptr;
    
        if (transport_type == "car") {
            unsigned int seat_number = sqlite3_column_int(stmt, 19);
            transport = new Car(title, image, engine_volume, mileage, weight, year, seat_number);
        }
        else if (transport_type == "truck") {
            unsigned int load_capacity = sqlite3_column_int(stmt, 20);
            transport = new Truck(title, image, engine_volume, mileage, weight, year, load_capacity);
        }
        else if (transport_type == "boat") {
            unsigned int propeller_number = sqlite3_column_int(stmt, 21);
            transport = new Boat(title, image, engine_volume, mileage, weight, year, propeller_number);
        }
    
        adverts.emplace_back(account, transport, slug, price, city, description, created, updated);
    }
    
    if (!_sort_by.empty()) {
        MergeSort(adverts, _sort_by);
    }
    
    sqlite3_finalize(stmt);
    return adverts;
}

Advert* Database::get_advert_by_slug(const std::string& _slug) {
    sqlite3_stmt* stmt;
    const char* query =
        "SELECT a.slug, a.price, a.city, a.description, a.created, a.updated,"
        "ac.username, ac.password, ac.first_name, ac.last_name, ac.email, ac.phone, "
        "t.title, t.image, t.engine_volume, t.mileage, t.weight, t.year, "
        "CASE "
        "WHEN tc.transport_ptr_id IS NOT NULL THEN 'car' "
        "WHEN tt.transport_ptr_id IS NOT NULL THEN 'truck' "
        "WHEN tb.transport_ptr_id IS NOT NULL THEN 'boat' "
        "END AS transport_type, "
        "tc.seat_number, tt.load_capacity, tb.propeller_number "
        "FROM main_advert a "
        "JOIN account ac ON a.account_id = ac.id "
        "JOIN main_transport t ON a.transport_id = t.id "
        "LEFT JOIN main_car tc ON t.id = tc.transport_ptr_id "
        "LEFT JOIN main_truck tt ON t.id = tt.transport_ptr_id "
        "LEFT JOIN main_boat tb ON t.id = tb.transport_ptr_id "
        "WHERE a.slug = ?";

    if (sqlite3_prepare_v2(db, query, -1, &stmt, nullptr) != SQLITE_OK) {
        std::cerr << "Failed to fetch advert: " << sqlite3_errmsg(db) << std::endl;
        return nullptr;
    }

    sqlite3_bind_text(stmt, 1, _slug.c_str(), -1, SQLITE_STATIC);

    if (sqlite3_step(stmt) != SQLITE_ROW) {
        sqlite3_finalize(stmt);
        return nullptr;
    }

    std::string slug = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 0));
    unsigned int price = sqlite3_column_int(stmt, 1);
    std::string city = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 2));
    std::string description = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 3));
    std::string created = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 4));
    std::string updated = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 5));

    std::string username = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 6));
    std::string password = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 7));
    std::string first_name = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 8));
    std::string last_name = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 9));
    std::string email = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 10));
    std::string phone = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 11));

    std::string title = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 12));
    std::string image = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 13));
    double engine_volume = sqlite3_column_double(stmt, 14);
    unsigned int mileage = sqlite3_column_int(stmt, 15);
    unsigned int weight = sqlite3_column_int(stmt, 16);
    unsigned int year = sqlite3_column_int(stmt, 17);

    std::string transport_type = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 18));

    Account* account = new Account(username, password, first_name, last_name, email, phone);
    Transport* transport = nullptr;

    if (transport_type == "car") {
        unsigned int seats_number = sqlite3_column_int(stmt, 19);
        transport = new Car(title, image, engine_volume, mileage, weight, year, seats_number);
    }
    else if (transport_type == "truck") {
        unsigned int load_capacity = sqlite3_column_int(stmt, 20);
        transport = new Truck(title, image, engine_volume, mileage, weight, year, load_capacity);
    }
    else if (transport_type == "boat") {
        unsigned int propeller_number = sqlite3_column_int(stmt, 21);
        transport = new Boat(title, image, engine_volume, mileage, weight, year, propeller_number);
    }

    sqlite3_finalize(stmt);
    return new Advert(account, transport, slug, price, city, description, created, updated);
}

void Database::MergeSort(std::list<Advert>& adverts, const std::string& sort_by) {
    if (adverts.size() <= 1) return;

    std::list<Advert> left, right;
    auto middle = adverts.begin();
    std::advance(middle, adverts.size() / 2);

    left.splice(left.end(), adverts, adverts.begin(), middle);
    right.splice(right.end(), adverts, middle, adverts.end());

    MergeSort(left, sort_by);
    MergeSort(right, sort_by);
    merge(left, right, adverts, sort_by);
}

void Database::merge(std::list<Advert>& left, std::list<Advert>& right, std::list<Advert>& adverts, const std::string& sort_by) {
    auto leftPtr = left.begin();
    auto rightPtr = right.begin();

    while (leftPtr != left.end() && rightPtr != right.end()) {
        bool flag = false;

        if (sort_by == "date_desc") {
            flag = leftPtr->created >= rightPtr->created;
        }
        else if (sort_by == "date_asc") {
            flag = leftPtr->created <= rightPtr->created;
        }
        else if (sort_by == "year_asc") {
            flag = leftPtr->transport->year <= rightPtr->transport->year;
        }
        else if (sort_by == "year_desc") {
            flag = leftPtr->transport->year >= rightPtr->transport->year;
        }
        else if (sort_by == "price_asc") {
            flag = leftPtr->price <= rightPtr->price;
        }
        else if (sort_by == "price_desc") {
            flag = leftPtr->price >= rightPtr->price;
        }

        if (flag) {
            adverts.push_back(*leftPtr);
            ++leftPtr;
        }
        else {
            adverts.push_back(*rightPtr);
            ++rightPtr;
        }
    }

    adverts.splice(adverts.end(), left, leftPtr, left.end());
    adverts.splice(adverts.end(), right, rightPtr, right.end());
}

PYBIND11_MODULE(database, m) {
    py::class_<Transport>(m, "Transport")
        .def_readonly("title", &Transport::title)
        .def_readonly("image", &Transport::image)
        .def_readonly("engine_volume", &Transport::engine_volume)
        .def_readonly("mileage", &Transport::mileage)
        .def_readonly("weight", &Transport::weight)
        .def_readonly("year", &Transport::year);

    py::class_<Car, Transport>(m, "Car")
        .def_readonly("seat_number", &Car::seat_number);

    py::class_<Truck, Transport>(m, "Truck")
        .def_readonly("load_capacity", &Truck::load_capacity);

    py::class_<Boat, Transport>(m, "Boat")
        .def_readonly("propeller_number", &Boat::propeller_number);

    py::class_<Account>(m, "Account")
        .def_readonly("username", &Account::username)
        .def_readonly("password", &Account::password)
        .def_readonly("first_name", &Account::first_name)
        .def_readonly("last_name", &Account::last_name)
        .def_readonly("email", &Account::email)
        .def_readonly("phone", &Account::phone);

    py::class_<Advert>(m, "Advert")
        .def("get_absolute_url", &Advert::get_absolute_url)
        .def_readonly("slug", &Advert::slug)
        .def_readonly("price", &Advert::price)
        .def_readonly("city", &Advert::city)
        .def_readonly("description", &Advert::description)
        .def_readonly("created", &Advert::created)
        .def_readonly("updated", &Advert::updated)
        .def_readonly("transport", &Advert::transport)
        .def_readonly("account", &Advert::account);

    py::class_<Database>(m, "Database")
        .def(py::init<const std::string&>(), py::arg("db_name") = "db.sqlite3")
        .def("get_adverts", &Database::get_adverts,
            py::arg("_username") = "", 
            py::arg("_sort_by") = "", 
            py::arg("_transport_type") = "all", 
            py::arg("_title") = "", 
            py::arg("_year") = 0, 
            py::arg("_city") = "", 
            py::arg("_min_price") = 0, 
            py::arg("_max_price") = 0)
        .def("get_advert_by_slug", &Database::get_advert_by_slug);
}