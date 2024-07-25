using Telegram.Bot;
using Telegram.Bot.Exceptions;
using Telegram.Bot.Extensions.Polling;
using Telegram.Bot.Types;
using Telegram.Bot.Types.Enums;
using Telegram.Bot.Types.ReplyMarkups;

// Store bot screaming status
var screaming = false;

// Pre-assign menu text
const string firstMenu = "<b>Menu 1</b>\n\nA beautiful menu with a shiny inline button.";
const string secondMenu = "<b>Menu 2</b>\n\nA better menu with even more shiny inline buttons.";

// Pre-assign button text
const string nextButton = "Next";
const string backButton = "Back";
const string tutorialButton = "Tutorial";


// Build keyboards
InlineKeyboardMarkup firstMenuMarkup = new(InlineKeyboardButton.WithCallbackData(nextButton));
InlineKeyboardMarkup secondMenuMarkup = new(
    new[] {
        new[] { InlineKeyboardButton.WithCallbackData(backButton) },
        new[] { InlineKeyboardButton.WithUrl(tutorialButton, "https://core.telegram.org/bots/tutorial") }
    }
);

// StartReceiving does not block the caller thread. Receiving is done on the ThreadPool, so we use cancellation token
bot.StartReceiving(
    updateHandler: HandleUpdate,
    errorHandler: HandleError,
    cancellationToken: cts.Token
);

// Tell the user the bot is online
Console.WriteLine("Start listening for updates. Press enter to stop");
Console.ReadLine();

// Send cancellation request to stop the bot
cts.Cancel();

// Each time a user interacts with the bot, this method is called
async Task HandleUpdate(ITelegramBotClient _, Update update, CancellationToken cancellationToken)
{
    switch (update.Type)
    {
        // A message was received
        case UpdateType.Message:
            await HandleMessage(update.Message!);
            break;

        // A button was pressed
        case UpdateType.CallbackQuery:
            await HandleButton(update.CallbackQuery!);
            break;
    }
}

async Task HandleError(ITelegramBotClient _, Exception exception, CancellationToken cancellationToken)
{
    await Console.Error.WriteLineAsync(exception.Message);
}

async Task HandleMessage(Message msg)
{
    var user = msg.From;
    var text = msg.Text ?? string.Empty;

    if (user is null)
        return;

    // Print to console
    Console.WriteLine($"{user.FirstName} wrote {text}");

    // When we get a command, we react accordingly
    if (text.StartsWith("/"))
    {
        await HandleCommand(user.Id, text);
    }
    else if (screaming && text.Length > 0)
    {
        // To preserve the markdown, we attach entities (bold, italic..)
        await bot.SendTextMessageAsync(user.Id, text.ToUpper(), entities: msg.Entities);
    }
    else
    {   // This is equivalent to forwarding, without the sender's name
        await bot.CopyMessageAsync(user.Id, user.Id, msg.MessageId);
    }
}


async Task HandleCommand(long userId, string command)
{
    switch (command)
    {
        case "/scream":
            screaming = true;
            break;

        case "/whisper":
            screaming = false;
            break;

        case "/menu":
            await SendMenu(userId);
            break;
    }

    await Task.CompletedTask;
}

async Task SendMenu(long userId)
{
    await bot.SendTextMessageAsync(
    userId,
    firstMenu,
    (int)ParseMode.Html,
    replyMarkup: firstMenuMarkup
);
}

async Task HandleButton(CallbackQuery query)
{
    string text = string.Empty;
    InlineKeyboardMarkup markup = new(Array.Empty<InlineKeyboardButton>());

    if (query.Data == nextButton)
    {
        text = secondMenu;
        markup = secondMenuMarkup;
    }
    else if (query.Data == backButton)
    {
        text = firstMenu;
        markup = firstMenuMarkup;
    }

    // Close the query to end the client-side loading animation
    await bot.AnswerCallbackQueryAsync(query.Id);

    // Replace menu text and keyboard
    await bot.EditMessageTextAsync(
        query.Message!.Chat.Id,
        query.Message.MessageId,
        text,
        ParseMode.Html,
        replyMarkup: markup
    );
}