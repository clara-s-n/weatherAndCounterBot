// CounterService.cs
namespace Library;
using System;

public class CounterService
{
    private int _counter = 1;

    public async Task IncrementCounter(Message message)
    {
        _counter++;
        //await SendMessage(message, $"El contador actual es {_counter}");
    }
}