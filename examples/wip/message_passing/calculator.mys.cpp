// This file was generated by mys. DO NOT EDIT!!!

#include "message_passing/calculator.mys.hpp"
#include "message_passing/student.mys.hpp"

namespace message_passing::calculator
{

Add::Add(float first, float second)
{
    this->first = first;
    this->second = second;
}

Add::~Add()
{
}

Result::Result(float result)
{
    this->result = result;
}

Result::~Result()
{
}

Calculator::Calculator()
{
    this->student = std::nullopt;
}

Calculator::~Calculator()
{
}

void Calculator::send_add(std::shared_ptr<Add>& message)
{
}

void Calculator::handle_add(std::shared_ptr<Add>& message)
{
    std::cout << *message << std::endl;
    auto value = std::make_shared<Result>(message->first + message->second);
    this->student.value()->send_result(value);
}

}
