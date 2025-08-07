from prefect import task, flow

@task
def generate_greeting_text():
    text = "Hello there! Nice to have you around!"
    return text

@flow
def greeting_procedure():
    text = generate_greeting_text()
    more_text = "Let's try out Prefect in this script ...!"
    return text + " " + more_text

if __name__ == "__main__":
    greeting_procedure()