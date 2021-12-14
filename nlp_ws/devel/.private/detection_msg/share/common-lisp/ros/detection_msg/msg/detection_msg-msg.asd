
(cl:in-package :asdf)

(defsystem "detection_msg-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "objMessage" :depends-on ("_package_objMessage"))
    (:file "_package_objMessage" :depends-on ("_package"))
  ))