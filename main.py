import yt
import os
import sys
import yt
from glob import glob
import matplotlib.pyplot as plt

def plot_2D(output, Ey, Ez, rho, y, z):
    fig = plot.figure(figsize=np.array((240, 240)) / 72)
    ax = fig.add_subplot(1, 1, 1, aspect=1.0)

    ax.set_xlabel('$z$ (um)', labelpad=0.0)
    ax.set_ylabel('$y$ (um)', labelpad=0.0)

    Y, Z = np.meshgrid(
        np.linspace(-50.0, 50.0, 64),
        np.linspace(-100.0, 100.0, 128))
    ax.quiver(
        Z[::4, ::4], Y[::4, ::4],
        Ez[::4, ::4].T, Ey[::4, ::4].T,
        scale=1e9, minlength=0.1,
        width=0.002,
        headwidth=2.5, headlength=4.5, headaxislength=4)
    ax.imshow(
        -rho[::1, ::1], cmap=blue_cmap,
        extent=(-100.0, 100.0, -50.0, 50))

    ax.quiver(
        Z[::4, ::4], Y[::4, ::4],
        Ez[::4, ::4].T, Ey[::4, ::4].T,
        scale=1e10, minlength=0.1,
        width=0.002,
        headwidth=2.5, headlength=4.5, headaxislength=4)
    # *xlims, *ylims))
    # d.sim.XMIN[0]/um, d.sim.XMAX[0]/um,
    # d.sim.XMIN[1]/um, d.sim.XMAX[1]/um))

    ax.plot(
        z[::2] / um, y[::2] / um,
        marker='.', ls='', markersize=0.001, color='k', alpha=0.1)
    # ax.text(
    #     # 0.05, 0.9, f'$ct = {c_light*time/um:.3f}\;\mu m$', va='center',
    #     0.05, 0.9, f'ct = {c_light*time/um:.3f} um', va='center',
    #     size=6.0, transform=ax.transAxes)

    ax.xaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator())
    ax.yaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator())

    output.savefig(fig, transparent=True)

def main():
    for filename in glob('diags_rz/diag*')[1:]:
        print(filename)
        # Loop through simulation data files
        ds = yt.load(filename)
        # Load data from the current file using yt
        #slc = yt.SlicePlot(ds,2,'rho',origin='native')
        # Create slice plots for both datasets
        slc1 = yt.SlicePlot(ds,2,'rho',origin='native')
        slc2 = yt.SlicePlot(ds,2,'Ez',origin='native')

        # Adjust the alpha channel of the color map for each field
        # Opacity values are between 0 and 1 (0 = fully transparent, 1 = fully opaque)
        alpha1 = 0.5  # Adjust as needed
        alpha2 = 0.7  # Adjust as needed


        # Modify the alpha channel for field 'rho' in the first slice plot
        slc1.plots['rho'].cb.set_alpha(0.5)
        slc2.plots['Ez'].cb.set_alpha(0.7)

        # Create a combined plot using matplotlib
        fig, ax = plt.subplots()
        #slc1.plots['rho'].annotate_text((0.05, 0.95), 'Field 1', coord_system='axes', text_args={'color': 'white'})
        #slc1.plots['rho'].annotate_text((0.05, 0.9), 'Opacity: 50%', coord_system='axes', text_args={'color': 'white'})
        slc1.plots['rho'].display(fig=fig, axes=ax)

        #slc2.plots['Ez'].annotate_text((0.05, 0.85), 'Field 2', coord_system='axes', text_args={'color': 'white'})
        #slc2.plots['Ez'].annotate_text((0.05, 0.8), 'Opacity: 70%', coord_system='axes', text_args={'color': 'white'})
        slc2.plots['Ez'].display(fig=fig, axes=ax)
        # Show the plot
        plt.show()




        # Show the overlaid plot
        #overlaid_plot.save()
        '''
        A = ds.covering_grid(
            level=0, left_edge=ds.domain_left_edge, dims=ds.domain_dimensions)
        print(A)
        # Create a covering grid for the dataset
        rho = [A[x].to_ndarray() for x in ['rho']]
        # Extract charge density data
        ad = ds.all_data()
        x, y, z = [
            ad['driver', 'particle_position_' + x].to_ndarray()
            for x in ['x', 'y', 'z']]
        z = z - ds.domain_center.value[2]
        # Extract spatial coordinates and adjust 'z'
        plot_2D(output, Ey[16], Ez[16], rho[16], y, z)
        # Call 'plot_2D' function to create and save the 2D plot
    output.close()
    '''

if __name__ == '__main__':
    sys.exit(main())