#ifndef MYS_BUILTIN_ERRORS
#define MYS_BUILTIN_ERRORS

#include "../mys.hpp"

// The Error trait that all errors must implement.
class Error : public Object {
public:
    // Throw the C++ exception. Needed when re-raising the exception.
    [[ noreturn ]] virtual void __throw() = 0;
};

class TypeError : public Error, public std::enable_shared_from_this<TypeError> {
public:
    String m_message;
    TypeError()
    {
    }
    TypeError(const String& message) : m_message(message)
    {
    }
    virtual ~TypeError()
    {
    }
    [[ noreturn ]] void __throw();
};

class __TypeError final : public std::exception {
public:
    std::shared_ptr<TypeError> m_error;
    __TypeError(const std::shared_ptr<TypeError>& error) : m_error(error)
    {
    }
};

class ValueError : public Error, public std::enable_shared_from_this<ValueError> {
public:
    String m_message;
    ValueError()
    {
    }
    ValueError(const String& message) : m_message(message)
    {
    }
    virtual ~ValueError()
    {
    }
    [[ noreturn ]] void __throw();
};

class __ValueError final : public std::exception {
public:
    std::shared_ptr<ValueError> m_error;
    __ValueError(const std::shared_ptr<ValueError>& error) : m_error(error)
    {
    }
};

class GeneralError : public Error, public std::enable_shared_from_this<GeneralError> {
public:
    String m_message;
    GeneralError()
    {
    }
    GeneralError(const String& message) : m_message(message)
    {
    }
    virtual ~GeneralError()
    {
    }
    [[ noreturn ]] void __throw();
};

class __GeneralError final : public std::exception {
public:
    std::shared_ptr<GeneralError> m_error;
    __GeneralError(const std::shared_ptr<GeneralError>& error) : m_error(error)
    {
    }
};

class NoneError : public Error, public std::enable_shared_from_this<NoneError> {
public:
    String m_message;
    NoneError()
    {
    }
    NoneError(const String& message) : m_message(message)
    {
    }
    virtual ~NoneError()
    {
    }
    [[ noreturn ]] void __throw();
};

class __NoneError final : public std::exception {
public:
    std::shared_ptr<NoneError> m_error;
    __NoneError(const std::shared_ptr<NoneError>& error) : m_error(error)
    {
    }
};

class KeyError : public Error, public std::enable_shared_from_this<KeyError> {
public:
    String m_message;
    KeyError()
    {
    }
    KeyError(const String& message) : m_message(message)
    {
    }
    virtual ~KeyError()
    {
    }
    [[ noreturn ]] void __throw();
};

class __KeyError final : public std::exception {
public:
    std::shared_ptr<KeyError> m_error;
    __KeyError(const std::shared_ptr<KeyError>& error) : m_error(error)
    {
    }
};

class IndexError : public Error, public std::enable_shared_from_this<IndexError> {
public:
    String m_message;
    IndexError()
    {
    }
    IndexError(const String& message) : m_message(message)
    {
    }
    virtual ~IndexError()
    {
    }
    [[ noreturn ]] void __throw();
};

class __IndexError final : public std::exception {
public:
    std::shared_ptr<IndexError> m_error;
    __IndexError(const std::shared_ptr<IndexError>& error) : m_error(error)
    {
    }
};

class NotImplementedError
    : public Error, public std::enable_shared_from_this<NotImplementedError> {
public:
    String m_message;
    NotImplementedError()
    {
    }
    NotImplementedError(const String& message) : m_message(message)
    {
    }
    virtual ~NotImplementedError()
    {
    }
    [[ noreturn ]] void __throw();
};

class __NotImplementedError final : public std::exception {
public:
    std::shared_ptr<NotImplementedError> m_error;
    __NotImplementedError(const std::shared_ptr<NotImplementedError>& error)
        : m_error(error)
    {
    }
};

class ZeroDivisionError
    : public Error, public std::enable_shared_from_this<ZeroDivisionError> {
public:
    String m_message;
    ZeroDivisionError()
    {
    }
    ZeroDivisionError(const String& message) : m_message(message)
    {
    }
    virtual ~ZeroDivisionError()
    {
    }
    [[ noreturn ]] void __throw();
};

class __ZeroDivisionError final : public std::exception {
public:
    std::shared_ptr<ZeroDivisionError> m_error;
    __ZeroDivisionError(const std::shared_ptr<ZeroDivisionError>& error)
        : m_error(error)
    {
    }
};

class AssertionError
    : public Error, public std::enable_shared_from_this<AssertionError> {
public:
    String m_message;
    AssertionError()
    {
    }
    AssertionError(const String& message) : m_message(message)
    {
    }
    virtual ~AssertionError()
    {
    }
    [[ noreturn ]] void __throw();
};

class __AssertionError final : public std::exception {
public:
    std::shared_ptr<AssertionError> m_error;
    __AssertionError(const std::shared_ptr<AssertionError>& error)
        : m_error(error)
    {
    }
};

class SystemExitError
    : public Error, public std::enable_shared_from_this<SystemExitError> {
public:
    String m_message;
    SystemExitError()
    {
    }
    SystemExitError(const String& message) : m_message(message)
    {
    }
    virtual ~SystemExitError()
    {
    }
    [[ noreturn ]] void __throw();
};

class __SystemExitError final : public std::exception {
public:
    std::shared_ptr<SystemExitError> m_error;
    __SystemExitError(const std::shared_ptr<SystemExitError>& error)
        : m_error(error)
    {
    }
};
#endif
