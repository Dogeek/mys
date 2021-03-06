#ifndef __MYSTYPESTRINGHPP
#define __MYSTYPESTRINGHPP

#include "../common.hpp"
#include "number.hpp"
#include "bool.hpp"
#include "char.hpp"
#include "bytes.hpp"

template <typename T> class List;

class Regex;
class RegexMatch;

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
    std::shared_ptr<List<String>> split(const Regex& regex) const;
    String join(const std::shared_ptr<List<String>>& list) const;
    void strip(std::optional<const String> chars) const;
    void strip_left(std::optional<const String> chars) const;
    void strip_right(std::optional<const String> chars) const;
    void lower() const;
    void upper() const;
    void casefold() const;
    void capitalize() const;
    i64 find(const String& sub, std::optional<i64> start, std::optional<i64> end) const;
    i64 find(const Char& sub, std::optional<i64> start, std::optional<i64> end) const;
    i64 find_reverse(const String& sub, std::optional<i64> start, std::optional<i64> end) const;
    i64 find_reverse(const Char& sub, std::optional<i64> start, std::optional<i64> end) const;
    String cut(const Char& chr) const;
    void replace(const Char& old, const Char& _new) const;
    void replace(const String& old, const String& _new) const;
    void replace(const Regex& regex, const String& replacement, int flags = 0) const;
    Bool is_digit() const;
    Bool is_numeric() const;
    Bool is_alpha() const;
    Bool is_space() const;
    RegexMatch match(const Regex& regex) const;

    int __len__() const;

    String __str__();

    i64 __int__() const;
};

std::ostream&
operator<<(std::ostream& os, const String& obj);

namespace std
{
    template<> struct hash<String>
    {
        std::size_t operator()(String const& s) const noexcept
        {
            // ToDo
            return 0;
        }
    };
}

static inline String operator*(int value, const String& string)
{
    return string * value;
}

static inline String operator+(const char *value_p, const String& string)
{
    String res(value_p);

    res += string;

    return res;
}

static inline String operator+(const String& string_1, const String& string_2)
{
    String res(string_1);

    res += string_2;

    return res;
}

const String& string_not_none(const String& obj);

#endif
