module.exports = function (grunt) {
  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    copy: {
      main: {
        files: [
          {
            expand: true,
            flatten: true,
            src: [
              'node_modules/xterm/dist/xterm.css',
              'src/css/style.css'
            ],
            dest: 'public/src/css'
          },
          {
            expand: true,
            flatten: true,
            src: [
              'node_modules/xterm/dist/xterm.js',
              'node_modules/xterm/dist/xterm.js.map',
              'node_modules/xterm/dist/addons/fit/fit.js',
              'node_modules/socket.io/node_modules/socket.io-client/dist/socket.io.js',
              'node_modules/socket.io/node_modules/socket.io-client/dist/socket.io.js.map',
              'src/js/client.js'
            ],
            dest: 'public/src/js'
          }
        ]
      }
    },
    concat: {
      options: {
        sourceMap: true,
        sourceMapName: 'public/src/webssh2.concat.map',
        sourceMapStyle: 'embed'
      },
      css: {
        src: ['public/src/css/*.css'],
        dest: 'public/webssh2.css'
      },
      js: {
        src: [
          'public/src/js/xterm.js',
          'public/src/js/fit.js',
          'public/src/js/socket.io.js',
          'public/src/js/client.js'
        ],
        dest: 'public/webssh2.js'
      }
    },
    uglify: {
      options: {
        banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n',
        sourceMap: true,
        sourceMapName: 'public/src/webssh2.min.map'
      },
      build: {
        src: ['public/src/js/xterm.js', 'public/src/js/fit.js', 'public/src/js/socket.io.js', 'public/src/js/client.js'],
        dest: 'public/webssh2.min.js'
      }
    }
  })

  // Load the plugin that provides the "uglify" task.
  grunt.loadNpmTasks('grunt-contrib-copy')
  grunt.loadNpmTasks('grunt-contrib-concat')
  grunt.loadNpmTasks('grunt-contrib-uglify')

  // Default task(s).
  grunt.registerTask('default', ['copy', 'concat', 'uglify'])
}
