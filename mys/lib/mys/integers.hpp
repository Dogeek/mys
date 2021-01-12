#ifndef MYS_BUILTIN_INTEGERS
#define MYS_BUILTIN_INTEGERS

#include <iostream>


typedef int8_t i8;
typedef int16_t i16;
typedef int32_t i32;
typedef int64_t i64;
typedef uint8_t u8;
typedef uint16_t u16;
typedef uint32_t u32;
typedef uint64_t u64;
typedef float f32;
typedef double f64;

// To make str(bool) and print(bool) show True and False.
struct Bool {
    bool m_value;

    Bool() : m_value(false)
    {
    }

    Bool(bool value) : m_value(value)
    {
    }

    operator bool() const
    {
        return m_value;
    }
};

// Integer power (a ** b).
template <typename TB, typename TE>
TB ipow(TB base, TE exp)
{
    TB result = 1;

    while (exp != 0) {
        if ((exp & 1) == 1) {
            result *= base;
        }

        exp >>= 1;
        base *= base;
    }

    return result;
}
#endif
