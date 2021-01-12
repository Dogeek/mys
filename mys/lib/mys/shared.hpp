#ifndef MYS_BUILTIN_SHARED
#define MYS_BUILTIN_SHARED

#include "../mys.hpp"

template <typename T>
using SharedList = std::shared_ptr<List<T>>;

template <class ...T>
using SharedTuple = std::shared_ptr<Tuple<T...>>;

template <typename TK, typename TV>
using SharedDict = std::shared_ptr<Dict<TK, TV>>;

#endif
