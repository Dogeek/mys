// This file was generated by mys. DO NOT EDIT!!!

#pragma once

#include "mys.hpp"

namespace mys::basics
{
class Calc;
Tuple<i32, String> func_1(i32 a);
#define MYS_BASICS_func_1_IMPORT_AS(__name__) \
    constexpr auto __name__ = [] (auto &&...args) { \
        return mys::basics::func_1(std::forward<decltype(args)>(args)...); \
    };
i32 func_2(i32 a, i32 b = 1);
#define MYS_BASICS_func_2_IMPORT_AS(__name__) \
    constexpr auto __name__ = [] (auto &&...args) { \
        return mys::basics::func_2(std::forward<decltype(args)>(args)...); \
    };
std::shared_ptr<Dict<i32, std::shared_ptr<List<f32>>>> func_3(i32 a);
#define MYS_BASICS_func_3_IMPORT_AS(__name__) \
    constexpr auto __name__ = [] (auto &&...args) { \
        return mys::basics::func_3(std::forward<decltype(args)>(args)...); \
    };
void func_4(void);
#define MYS_BASICS_func_4_IMPORT_AS(__name__) \
    constexpr auto __name__ = [] (auto &&...args) { \
        return mys::basics::func_4(std::forward<decltype(args)>(args)...); \
    };
std::shared_ptr<List<i64>> func_5(void);
#define MYS_BASICS_func_5_IMPORT_AS(__name__) \
    constexpr auto __name__ = [] (auto &&...args) { \
        return mys::basics::func_5(std::forward<decltype(args)>(args)...); \
    };
}
