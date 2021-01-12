#ifndef MYS_BUITLIN_STRING
#define MYS_BUILTIN_STRING

#include <iostream>
#include <optional>

#include "integers.hpp"
#include "bytes.hpp"
#include "utils.hpp"
#include "char.hpp"

template<typename T>
class List final;

// A string.
class String final {
private:
    void strip_left_right(std::optional<const String> chars, bool left, bool right) const;
    void lower(bool capitalize) const;
    i64 find(const String& sub, std::optional<i64> start, std::optional<i64> end,
             bool reverse) const;

    enum class CaseMode { LOWER, UPPER, FOLD, CAPITALIZE };
    void set_case(CaseMode mode) const;

public:
    std::shared_ptr<std::vector<Char>> m_string;

    String() : m_string(nullptr)
    {
    }

    String(const char *str);

    String(const std::string& str) : String(str.c_str())
    {
    }

    String(std::initializer_list<Char> il) :
        m_string(std::make_shared<std::vector<Char>>(il))
    {
    }

    String(const Bytes& bytes) : m_string(nullptr)
    {
    }

    String(i8 value) : String(std::to_string(value))
    {
    }

    String(i16 value) : String(std::to_string(value))
    {
    }

    String(i32 value) : String(std::to_string(value))
    {
    }

    String(i64 value) : String(std::to_string(value))
    {
    }

    String(u8 value) : String(std::to_string(value))
    {
    }

    String(u16 value) : String(std::to_string(value))
    {
    }

    String(u32 value) : String(std::to_string(value))
    {
    }

    String(u64 value) : String(std::to_string(value))
    {
    }

    String(f32 value) : String(std::to_string(value))
    {
    }

    String(f64 value) : String(std::to_string(value))
    {
    }

    String(Bool value) : String(value ? "True" : "False")
    {
    }

    String(const Char& value) : String(std::initializer_list<Char>{value})
    {
    }

    void operator+=(const String& other) const
    {
        m_string->insert(m_string->end(),
                         other.m_string->begin(),
                         other.m_string->end());
    }

    void operator+=(const Char& other) const
    {
        m_string->push_back(other);
    }

    String operator+(const String& other);

    String operator*(int value) const;

    bool operator==(const String& other) const
    {
        if (m_string && other.m_string) {
            return *m_string == *other.m_string;
        } else {
            return (!m_string && !other.m_string);
        }
    }

    bool operator!=(const String& other) const
    {
        return !(*this == other);
    }

    bool operator<(const String& other) const
    {
        return *m_string < *other.m_string;
    }

    Bytes to_utf8() const;
    Char& get(i64 index) const;
    String get(std::optional<i64> start, std::optional<i64> end,
               i64 step) const;

    String to_lower() const;
    String to_upper() const;
    String to_casefold() const;
    String to_capitalize() const;
    Bool starts_with(const String& value) const;
    Bool ends_with(const String& value) const;
    std::shared_ptr<List<String>> split(const String& separator) const;
    String join(const std::shared_ptr<List<String>>& list) const;
    void strip(std::optional<const String> chars) const;
    void lstrip(std::optional<const String> chars) const;
    void rstrip(std::optional<const String> chars) const;
    void lower() const;
    void upper() const;
    void casefold() const;
    void capitalize() const;
    i64 find(const String& sub, std::optional<i64> start, std::optional<i64> end) const;
    i64 find(const Char& sub, std::optional<i64> start, std::optional<i64> end) const;
    i64 rfind(const String& sub, std::optional<i64> start, std::optional<i64> end) const;
    i64 rfind(const Char& sub, std::optional<i64> start, std::optional<i64> end) const;
    String cut(const Char& chr) const;
    void replace(const Char& old, const Char& _new) const;
    void replace(const String& old, const String& _new) const;
    Bool isdigit() const;
    Bool isnumeric() const;
    Bool isalpha() const;
    Bool isspace() const;

    int __len__() const;

    String __str__();

    i64 __int__() const;
};

static inline String operator*(int value, const String& string)
{
    return string * value;
}

std::ostream&
operator<<(std::ostream& os, const String& obj);

static inline String operator+(const char *value_p, const String& string)
{
    String res(value_p);

    res += string;

    return res;
}

const String& string_not_none(const String& obj);

String string_str(const String& value);

String bytes_str(const Bytes& value);

#endif
