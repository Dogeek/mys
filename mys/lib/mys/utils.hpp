#ifndef MYS_BUILTIN_UTILS
#define MYS_BUILTIN_UTILS

#include <iostream>

#include "integers.hpp"


template <typename T> const std::shared_ptr<T>&
shared_ptr_not_none(const std::shared_ptr<T>& obj);

size_t encode_utf8(char *dst_p, i32 ch);

#endif
