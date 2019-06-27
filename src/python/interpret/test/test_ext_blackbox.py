def test_import_demo_explainer():
    from interpret.ext.blackbox import DemoExplainer
    print("Loaded {}".format(DemoExplainer.__name__))
