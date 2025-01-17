#ifndef DATABASE_H
#define DATABASE_H

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <iostream>
#include <utility>
#include <string>
#include <list>
#include <sqlite3.h>

namespace py = pybind11;

class Transport {
public:
    std::string title;
    std::string image;
    double engine_volume;
    unsigned int mileage;
    unsigned int weight;
    unsigned int year;

    Transport(const std::string& title, const std::string& image, double engine_volume,
        unsigned int mileage, unsigned int weight, unsigned int year);
    virtual ~Transport() = 0;
};

class Car : public Transport {
public:
    unsigned int seat_number;

    Car(const std::string& title, const std::string& image, double engine_volume,
        unsigned int mileage, unsigned int weight, unsigned int year, unsigned int seat_number);
};

class Truck : public Transport {
public:
    unsigned int load_capacity;

    Truck(const std::string& title, const std::string& image, double engine_volume,
        unsigned int mileage, unsigned int weight, unsigned int year, unsigned int load_capacity);
};

class Boat : public Transport {
public:
    unsigned int propeller_number;

    Boat(const std::string& title, const std::string& image, double engine_volume, unsigned int mileage,
        unsigned int weight, unsigned int year, unsigned int propeller_number);
};

class Account {
public:
    std::string username;
    std::string password;
    std::string first_name;
    std::string last_name;
    std::string email;
    std::string phone;

    Account(const std::string& username, const std::string& password, const std::string& first_name,
        const std::string& last_name, const std::string& email, const std::string& phone);
};

class Advert {
public:
    Account* account;
    Transport* transport;
    std::string slug;
    unsigned int price;
    std::string city;
    std::string description;
    std::string created;
    std::string updated;

    Advert(Account* account, Transport* transport, const std::string& slug, unsigned int price,
        const std::string& city, const std::string& description, const std::string& created, const std::string& updated);
    std::string get_absolute_url();
};

class Database {
private:
    sqlite3* db;
    void merge(std::list<Advert>& left, std::list<Advert>& right,
        std::list<Advert>& adverts, const std::string& sort_by);
public:

    Database(const std::string& db_name);
    ~Database();

    std::list<Advert> get_adverts(const std::string& _username = "", const std::string& _sort_by = "", const std::string& _transport_type = "all",
        const std::string& _title = "", unsigned int _year = 0, const std::string& _city = "",
        unsigned int _min_price = 0, unsigned int _max_price = 0);
    
    Advert* get_advert_by_slug(const std::string& _slug);

    void MergeSort(std::list<Advert>& adverts, const std::string& sort_by);
};

#endif