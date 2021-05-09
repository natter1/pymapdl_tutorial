import pyvista as pv
from ansys.mapdl.core import launch_mapdl
from ansys.mapdl.core.mapdl_corba import MapdlCorba  # used as TypeHint to enable code insight
from pyvista import Plotter


def main():
    mapdl = launch_mapdl()
    print(mapdl)
    mapdl.units("SI")  # only for documentation - no influence on FEA

    # clear any potential data from previous FEA, and set element type and material data
    reset_mapdl(mapdl)

    # create geometry for beam
    create_geometry_v1(mapdl, segments=77)  # crash for segments > 77

    #plot_geometry(mapdl)
    # set E and Poisson ratio
    set_material(mapdl)

    # set bounding conditions
    set_boundary_conditions_v1(mapdl)

    mapdl.slashsolu()
    mapdl.antype("static")
    mapdl.solve()
    mapdl.post1()

    plot_results(mapdl)

    mapdl.exit()
    return


class Beam:  # using a class makes it easier and saver to acces values compared to global variables
    # geometry
    w = 10
    h = 2

    # mesh
    segments = 5

    # element type
    et_num = 1
    et = "plane183"

    # material number
    mat_num = 1
    E = 71e9
    pr = 0.3


def reset_mapdl(mapdl: MapdlCorba):
    mapdl.finish()
    mapdl.clear()


def create_geometry_v1(mapdl: MapdlCorba, width=Beam.w, height=Beam.h, segments=Beam.segments):
    mapdl.prep7()
    mapdl.blc4(xcorner=0, ycorner=0, width=Beam.w, height=Beam.h)  # creates keypoints, lines, area but not nodes
    mapdl.esize(size=min(width/segments, height/2))  # height/2 -> make sure, at least two segments along height
    mapdl.et(itype=Beam.et_num, ename=Beam.et)
    mapdl.mat(Beam.mat_num)
    mapdl.amesh("all")


def plot_geometry(mapdl: MapdlCorba, theme="document"):
    pv.set_plot_theme(theme)
    plotter = pv.Plotter(shape=(2, 2))
    mapdl.nplot(plotter=plotter, knum=True, color='')
    plotter.subplot(0, 1)
    mapdl.lplot(plotter=plotter, color='')#color_lines=True) # color="#000000")
    plotter.subplot(1, 0)
    mapdl.aplot(plotter=plotter, color='')
    plotter.subplot(1, 1)
    mapdl.eplot(plotter=plotter, color='')
    plotter.link_views()
    plotter.show(screenshot=True)
    plotter.screenshot(f'multiplot_example')
    return


def plot_results(mapdl: MapdlCorba, theme="document"):
    pv.set_plot_theme(theme)
    plotter = pv.Plotter(shape=(2, 2))
    mapdl.result.plot_nodal_stress(0, comp="x", show_displacement=True, cpos="xy", plotter=plotter, add_text=False)
    plotter.subplot(0, 1)
    mapdl.result.plot_nodal_stress(0, comp="y", show_displacement=True, cpos="xy", plotter=plotter, add_text=False)
    mapdl.result.plot_nodal_solution(0, comp='norm', show_displacement=True, lighting=False,
                                                  background='w', text_color='k', show_edges=True, cpos='xy',
                                                  add_text=False, plotter=plotter)
    plotter.subplot(1, 1)
    mapdl.result.plot_nodal_solution(0, comp='x', show_displacement=True, lighting=False,
                                                  background='w', text_color='k', show_edges=True, cpos='xy',
                                                  add_text=False, plotter=plotter)

    # mapdl.result.plot_nodal_displacement(0, show_displacement=True, cpos="xy")

    plotter.link_views()
    plotter.show(screenshot=True)
    plotter.screenshot(f'multiplot_results')
    return


def set_material(mapdl: MapdlCorba):
    mapdl.prep7()
    mapdl.mp("ex", mat=Beam.mat_num, c0=Beam.E)
    mapdl.mp("nuxy", Beam.mat_num, c0=Beam.pr)


def set_boundary_conditions_v1(mapdl: MapdlCorba):
    mapdl.nsel(item="loc", comp="x", vmin=0)
    mapdl.d("all", "all")

    mapdl.nsel(item="loc", comp="x", vmin=Beam.w)
    mapdl.nsel("r", item="loc", comp="y", vmin=0)
    # mapdl.nplot(knum=True, cpos='xy', color='')

    mapdl.f("all", "fy", 40e7)


if __name__ == '__main__':
    main()
