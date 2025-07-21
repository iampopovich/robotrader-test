Feature: Login
    A page alowed to login into the platform

    Scenario: Successful login
        Given I'm a user
        And I have an account
        When I go to the login page
        And I fill in the login form with valid credentials
        And I press the login button
        And I complete the verification form if it appears
        Then I should be logged in

    Scenario: Unsuccessful login
        Given I'm a user
        And I have an account
        When I go to the login page
        And I fill in the login form with invalid credentials
        And I press the login button
        Then I should see an error message indicating invalid credentials

    Scenario: Login with empty credentials
        Given I'm a user
        When I go to the login page
        And I fill in the login form with empty credentials
        And I press the login button
        Then I should see an error message indicating that credentials cannot be empty

    Scenario: Login with unexisting account
        Given I'm a user
        When I go to the login page
        And I fill in the login form with credentials for an account that does not exist
        And I press the login button
        Then I should see an error message indicating that the account does not exist