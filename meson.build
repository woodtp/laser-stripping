project('laser-stripping', 'cpp')

python = import('python').find_installation('python3')

pyorbit3_dep = dependency('pyorbit3', required: true)
pyorbit3_incbase = pyorbit3_dep.get_variable(pkgconfig: 'includedir') / 'pyorbit3'

# pyorbit3 headers reference each other with bare filenames like "Bunch.hh";
# add all its subdirectories so those transitive includes resolve.
pyorbit3_subdirs_result = run_command(
  'find', pyorbit3_incbase, '-type', 'd',
  check: false
).stdout().strip().split('\n')

pyorbit3_subdir_incs = []
foreach d : pyorbit3_subdirs_result
  pyorbit3_subdir_incs += include_directories(d)
endforeach

ls_sources = files([
  'ConeLFMode/ConeLFmode.cc',
  'ConeLFMode/wrap_cone_lf_mode.cc',
  'ContinuumSS/ContinuumSS.cc',
  'ContinuumSS/TDMcontinuum.cc',
  'ContinuumSS/wrap_continuum_ss.cc',
  'ContinuumSS/wrap_tdm_continuum.cc',
  'DensityMatrix/DensityMatrix.cc',
  'DensityMatrix/wrap_density_matrix.cc',
  'DiagonalDensityMatrix/DM_noLaserField.cc',
  'DiagonalDensityMatrix/wrap_DM_noLaserField.cc',
  'FringeField/FringeField.cc',
  'FringeField/wrap_fringe_field.cc',
  'FroissartStoraLF/FroissartStoraLF.cc',
  'FroissartStoraLF/wrap_froissart_stora_lf.cc',
  'HermiteGaussianLFmode/HermiteGaussianLFmode.cc',
  'HermiteGaussianLFmode/wrap_hermite_gaussian_lf_mode.cc',
  'HminusStripping/HminusStripping.cc',
  'HminusStripping/wrap_hminus_stripping.cc',
  'HydrogenStarkParam/HydrogenStarkParam.cc',
  'HydrogenStarkParam/wrap_hydrogen_stark_param.cc',
  'LS_utils/BaseLaserFieldSource.cc',
  'LS_utils/FieldOrientation.cc',
  'LS_utils/FieldRotation.cc',
  'LS_utils/wrap_laserstripping.cc',
  'LaserFieldContainer/LaserFieldContainer.cc',
  'LaserFieldContainer/wrap_las_field_container.cc',
  'Quad_EM_field/ConstEMfield.cc',
  'Quad_EM_field/QuadEMfield.cc',
  'Quad_EM_field/wrap_const_em_field.cc',
  'Quad_EM_field/wrap_quad_em_field.cc',
  'Record/PrintExtEffects.cc',
  'Record/RecordEvolution.cc',
  'Record/wrap_print_ext_effects.cc',
  'Record/wrap_record_evolution.cc',
  'RegularGridFS/RegularGridFS.cc',
  'RegularGridFS/wrap_regular_grid_fs.cc',
  'SNSstrippingMagnet/SNSstrippingMagnet.cc',
  'SNSstrippingMagnet/wrap_snsstrippingmagnet.cc',
  'SchrodingerEquation/SchrodingerEquation.cc',
  'SchrodingerEquation/wrap_schrodinger_equation.cc',
  'Stark/Stark.cc',
  'Stark/wrap_stark.cc',
  'TwoLevelAtom/TwoLevelAtom.cc',
  'TwoLevelAtom/wrap_two_level_atom.cc',
  'TwoLevelStrongField/StarkStrongField.cc',
  'TwoLevelStrongField/TwoLevelStrongField.cc',
  'TwoLevelStrongField/wrap_stark_strong_field.cc',
  'TwoLevelStrongField/wrap_two_level_strong_field.cc',
  'Walls/Walls.cc',
  'Walls/wrap_walls.cc',
])

ls_inc = include_directories([
  '.',
  'ConeLFMode',
  'ContinuumSS',
  'DensityMatrix',
  'DiagonalDensityMatrix',
  'FringeField',
  'FroissartStoraLF',
  'HermiteGaussianLFmode',
  'HminusStripping',
  'HydrogenStarkParam',
  'LS_utils',
  'LaserFieldContainer',
  'Quad_EM_field',
  'Record',
  'RegularGridFS',
  'SNSstrippingMagnet',
  'SchrodingerEquation',
  'Stark',
  'TwoLevelAtom',
  'TwoLevelStrongField',
  'Walls',
])

python.extension_module('laserstripping',
  sources: ls_sources,
  include_directories: [ls_inc, pyorbit3_subdir_incs],
  dependencies: [pyorbit3_dep],
  install: true,
)
