from behave import *

from features.steps.support import JaxaContextInitialiser


@given("we use the JAXA client")
def step_impl(context):
    JaxaContextInitialiser(context=context)
