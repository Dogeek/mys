#ifndef MYS_BUILTIN_OPERATORS
#define MYS_BUILTIN_OPERATORS

template<typename T> bool
is(const std::shared_ptr<T>& a, const std::shared_ptr<T>& b)
{
    return a.get() == b.get();
}

template<typename T> bool
is(const std::shared_ptr<T>& a, void *b)
{
    return a.get() == nullptr;
}

template<typename T> bool
is(void *a, const std::shared_ptr<T>& b)
{
    return b.get() == nullptr;
}

// For nullptr == nullptr
static inline bool is(void *a, void *b)
{
    return a == b;
}

#endif
