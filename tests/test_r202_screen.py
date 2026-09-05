from sumui import GraphicsCommand, TextScreen;
import sumpy;


def test_aliases_keep_python_semantics():
    assert sumpy.TRUE is True and sumpy.true is True;
    assert sumpy.FALSE is False and sumpy.false is False;
    assert sumpy.NULL is None and sumpy.Null is None and sumpy.null is None;
    assert sumpy.NIL is None and sumpy.Nil is None and sumpy.nil is None and sumpy.none is None;


def test_dynamic_grid_cursor_and_graphics_facade():
    size=[80,25]; states=[]; commands=[];
    sumpy.set_text_screen(TextScreen(size_provider=lambda: tuple(size), cursor_setter=states.append));
    assert sumpy.cols()==80 and sumpy.rows()==25;
    size[:]=[41,17]; assert sumpy.cols()==41 and sumpy.rows()==17;
    assert sumpy.cursor(False)==0;
    assert sumpy.cursor(True)==1;
    assert sumpy.cursor("block")==2;
    sumpy.configure_graphics(lambda:(320,200,16), commands.append);
    assert (sumpy.gwidth(),sumpy.gheight(),sumpy.gcolors())==(320,200,16);
    command=sumpy.gprintf(10,20,"x=%d",7);
    assert isinstance(command,GraphicsCommand) and command.operation=="text" and command.arguments==(10,20,"x=7");
    sumpy.sort_layers("GRAPHICS","TEXT");
    assert commands[-1].operation=="sort_layers";


def test_r2021_border_width_emits_common_command():
    import sumpy.screen as screen;
    seen=[]; screen.configure_graphics(handler=seen.append);
    assert screen.border_width(18) == 18; assert screen.border_width() == 18;
    assert seen[-1].operation == "border_width" and seen[-1].arguments == (18,);
    screen.paper(0); screen.border(1);
    assert [item.operation for item in seen[-2:]] == ["paper","border"];
