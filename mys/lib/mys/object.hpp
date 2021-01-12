#ifndef MYS_BUILTIN_OBJECT
#define MYS_BUILTIN_OBJECT

#include "../mys.hpp"


class Object {
public:
    virtual void __format__(std::ostream& os) const;
    virtual String __str__();
};

template <typename T>
std::ostream& operator<<(std::ostream& os, const std::shared_ptr<T>& obj)
{
    if (obj) {
        os << *obj;
    } else {
        os << "None";
    }

    return os;
}

template <typename T>
std::ostream& operator<<(std::ostream& os, const std::vector<T>& obj)
{
    const char *delim_p;

    os << "[";
    delim_p = "";

    for (auto item = obj.begin(); item != obj.end(); item++, delim_p = ", ") {
        os << delim_p << *item;
    }

    os << "]";

    return os;
}

std::ostream& operator<<(std::ostream& os, const Bool& obj);

std::ostream& operator<<(std::ostream& os, Object& obj);


#endif
