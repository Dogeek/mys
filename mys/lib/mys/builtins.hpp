#ifndef MYS_BUILTIN_BUILTINS
#define MYS_BUILTIN_BUILTINS

#include <iostream>

#include "string.hpp"
#include "bytes.hpp"


template <typename T1, typename T2, typename... Tail>
auto vmin(T1&& v1, T2&& v2, Tail&&... tail)
{
    if constexpr (sizeof...(tail) == 0) {
        return v1 < v2 ? v1 : v2;
    } else {
        return vmin(vmin(v1, v2), tail...);
    }
}

template <typename T, typename... Tail>
auto min(T&& obj, Tail&&... tail)
{
    if constexpr (sizeof...(tail) == 0) {
        return obj->__min__();
    } else {
        return vmin(obj, tail...);
    }
}

template <typename T1, typename T2, typename... Tail>
auto vmax(T1&& v1, T2&& v2, Tail&&... tail)
{
    if constexpr (sizeof...(tail) == 0) {
        return v1 > v2 ? v1 : v2;
    } else {
        return vmax(vmax(v1, v2), tail...);
    }
}

template <typename T, typename... Tail>
auto max(T&& obj, Tail&&... tail)
{
    if constexpr (sizeof...(tail) == 0) {
        return obj->__max__();
    } else {
        return vmax(obj, tail...);
    }
}

template <typename T>
auto sum(const std::shared_ptr<T>& obj)
{
    return obj->__sum__();
}

template <typename TI, typename TC>
bool contains(const TI& item, const TC& container)
{
    return container->__contains__(item);
}

using std::abs;

class PrintString {
public:
    String m_value;

    PrintString(String value) : m_value(value) {}
};

std::ostream& operator<<(std::ostream& os, const PrintString& obj);

class PrintChar {
public:
    Char m_value;

    PrintChar(Char value) : m_value(value) {}
};

std::ostream& operator<<(std::ostream& os, const PrintChar& obj);

String input(String prompt);

#endif
