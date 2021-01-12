#ifndef __MYSHPP
#define __MYSHPP

#include <iostream>
#include <vector>
#include <memory>
#include <sstream>
#include <optional>

#include "robin_hood.hpp"

#include "mys/operators.hpp"
#include "mys/integers.hpp"
#include "mys/utils.hpp"

#include "mys/char.hpp"
#include "mys/bytes.hpp"

#include "mys/string.hpp"
#include "mys/errors.hpp"
#include "mys/object.hpp"
#include "mys/list.hpp"
#include "mys/dict.hpp"
#include "mys/tuple.hpp"
#include "mys/slices.hpp"


#include "mys/builtins.hpp"
#include "mys/shared.hpp"

// Exception output.
std::ostream& operator<<(std::ostream& os, const std::exception& e);

#define ASSERT(cond)                                            \
    if (!(cond)) {                                              \
        std::make_shared<AssertionError>(#cond)->__throw();     \
    }

#define assert_eq(v1, v2)                                               \
    if (!((v1) == (v2))) {                                              \
        std::cout << "Assert: " << (v1) << " != " << (v2) << std::endl; \
                                                                        \
        std::make_shared<AssertionError>("assert_eq failed")->__throw(); \
    }

class Test;

extern Test *tests_head_p;
extern Test *tests_tail_p;

typedef void (*test_func_t)(void);

class Test {

public:
    const char *m_name_p;
    test_func_t m_func;
    Test *m_next_p;

    Test(const char *name_p, test_func_t func);
};

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

    template<> struct hash<Bool>
    {
        std::size_t operator()(Bool const& s) const noexcept
        {
            return s.m_value;
        }
    };
}

template <typename T> const std::shared_ptr<T>&
shared_ptr_not_none(const std::shared_ptr<T>& obj)
{
    if (!obj) {
        std::make_shared<NoneError>("object is None")->__throw();
    }

    return obj;
}

std::shared_ptr<List<String>> create_args(int argc, const char *argv[]);

template<typename TK, typename TV>
std::shared_ptr<List<std::shared_ptr<Tuple<TK, TV>>>>
create_list_from_dict(const std::shared_ptr<Dict<TK, TV>>& dict)
{
    auto list = std::make_shared<List<std::shared_ptr<Tuple<TK, TV>>>>();

    for (auto const& [key, value] : shared_ptr_not_none(dict)->m_map) {
        list->append(std::make_shared<Tuple<TK, TV>>(key, value));
    }

    return list;
}

#endif
