Feature: Login
    A page alowed to login into the platform

    Scenario: Successful login
        Given I'm a user
        And I have an account
        When I go to the login page
        And I fill in the login form with valid credentials
        And I press the login button
        And I complete the verification form if it appears
        Then Dashboard should be displayed
