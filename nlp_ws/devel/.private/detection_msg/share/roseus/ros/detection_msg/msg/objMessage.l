;; Auto-generated. Do not edit!


(when (boundp 'detection_msg::objMessage)
  (if (not (find-package "DETECTION_MSG"))
    (make-package "DETECTION_MSG"))
  (shadow 'objMessage (find-package "DETECTION_MSG")))
(unless (find-package "DETECTION_MSG::OBJMESSAGE")
  (make-package "DETECTION_MSG::OBJMESSAGE"))

(in-package "ROS")
;;//! \htmlinclude objMessage.msg.html


(defclass detection_msg::objMessage
  :super ros::object
  :slots (_obj _score ))

(defmethod detection_msg::objMessage
  (:init
   (&key
    ((:obj __obj) "")
    ((:score __score) 0.0)
    )
   (send-super :init)
   (setq _obj (string __obj))
   (setq _score (float __score))
   self)
  (:obj
   (&optional __obj)
   (if __obj (setq _obj __obj)) _obj)
  (:score
   (&optional __score)
   (if __score (setq _score __score)) _score)
  (:serialization-length
   ()
   (+
    ;; string _obj
    4 (length _obj)
    ;; float64 _score
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _obj
       (write-long (length _obj) s) (princ _obj s)
     ;; float64 _score
       (sys::poke _score (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _obj
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _obj (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; float64 _score
     (setq _score (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get detection_msg::objMessage :md5sum-) "0ee8aa243ed15ae7496db1e213d462ca")
(setf (get detection_msg::objMessage :datatype-) "detection_msg/objMessage")
(setf (get detection_msg::objMessage :definition-)
      "string obj
float64 score
")



(provide :detection_msg/objMessage "0ee8aa243ed15ae7496db1e213d462ca")


